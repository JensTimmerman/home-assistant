"""Diagnostics support for the Guntamatic integration."""

from typing import Any

from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.redact import async_redact_data

from .const import DOMAIN
from .coordinator import GuntamaticConfigEntry
from .sensor import HEATING_CIRCUIT_REGEX

TO_REDACT = {CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: GuntamaticConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": entry.runtime_data.data,
    }


async def async_get_device_diagnostics(
    hass: HomeAssistant,
    entry: GuntamaticConfigEntry,
    device: dr.DeviceEntry,
) -> dict[str, Any]:
    """Return diagnostics for a device.

    Heating circuit devices only include the data of their own circuit.
    """
    coordinator = entry.runtime_data
    serial = coordinator.data["serial"][0]
    data = coordinator.data

    identifier = next((i[1] for i in device.identifiers if i[0] == DOMAIN), "")
    hc_prefix = f"{serial}_hc"
    if identifier.startswith(hc_prefix):
        circuit = identifier[len(hc_prefix) :]
        data = {
            key: value
            for key, value in data.items()
            if (match := HEATING_CIRCUIT_REGEX.match(key)) and match.group(1) == circuit
        }

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": data,
    }
