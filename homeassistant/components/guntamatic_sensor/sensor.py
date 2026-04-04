"""Support for Guntamatic sensors in Home Assistant."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GuntamaticConfigEntry
from .const import (
    DIAGNOSTIC_SENSORS,
    DOMAIN,
    SENSOR_DEVICE_CLASSES,
    SENSOR_STATE_CLASSES,
)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GuntamaticConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Guntamatic sensors from config entry."""
    data = entry.runtime_data
    coordinator = data.coordinator
    heater = data.heater

    known_sensors: set[str] = set()

    def _check_sensors() -> None:
        current_sensors = set(coordinator.data)
        new_sensors = current_sensors - known_sensors
        if new_sensors:
            known_sensors.update(new_sensors)
            async_add_entities(
                GuntamaticSensor(coordinator, name, heater.host) for name in new_sensors
            )

    _check_sensors()
    entry.async_on_unload(coordinator.async_add_listener(_check_sensors))


class GuntamaticSensor(CoordinatorEntity, SensorEntity):
    """Representation of a single Guntamatic sensor."""

    def __init__(self, coordinator, name, host):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = name
        self._attr_has_entity_name = True
        self._attr_name = name
        # serial might not be set on all devices
        serial = coordinator.data.get("Serial", [None])[0] or host

        self._attr_unique_id = (
            f"guntamatic_{serial.replace('.', '_')}_{name.replace(' ', '_')}"
        )
        unit = coordinator.data[name][1]  # unit
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = SENSOR_DEVICE_CLASSES.get(name)
        self._attr_state_class = SENSOR_STATE_CLASSES.get(name)

        self._attr_entity_category = (
            EntityCategory.DIAGNOSTIC if name in DIAGNOSTIC_SENSORS else None
        )

        # if no unit is given by the guntamatic, it's a string
        if not unit:
            self._attr_native_unit_of_measurement = None
            self._attr_state_class = None
            self._attr_device_class = None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name="Guntamatic Heater",
            manufacturer="Guntamatic",
            serial_number=serial if serial != host else None,
            sw_version=coordinator.data.get("Version", [None])[0],
        )

    @property
    def native_value(self):
        """Return the current value of the sensor."""
        return self.coordinator.data[self._attr_name][0]

    @property
    def native_unit_of_measurement(self):
        """Return the current unit of the sensor."""
        return self.coordinator.data[self._attr_name][1]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self._name in self.coordinator.data
