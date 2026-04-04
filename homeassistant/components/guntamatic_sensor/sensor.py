"""Support for Guntamatic sensors in Home Assistant."""

from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

UPDATE_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Guntamatic sensors from config entry."""

    data = entry.runtime_data
    coordinator = data.coordinator
    heater = data.heater

    # Create one entity per sensor
    sensors = [
        GuntamaticSensor(coordinator, name, heater.host) for name in coordinator.data
    ]

    async_add_entities(sensors)


class GuntamaticSensor(CoordinatorEntity, SensorEntity):
    """Representation of a single Guntamatic sensor."""

    def __init__(self, coordinator, name, host):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = name
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = (
            f"guntamatic_{host.replace('.', '_')}_{name.replace(' ', '_')}"
        )
        self._attr_native_unit_of_measurement = coordinator.data[name][1]  # unit
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.entry.entry_id)},
            "name": "Guntamatic Heater",
            "manufacturer": "Guntamatic",
        }

    @property
    def native_value(self):
        """Return the current value of the sensor."""
        return self.coordinator.data[self._attr_name][0]

    @property
    def native_unit_of_measurement(self):
        """Return the current unit of the sensor."""
        return self.coordinator.data[self._attr_name][1]
