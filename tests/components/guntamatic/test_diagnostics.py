"""Tests for the Guntamatic diagnostics."""

import pytest
from syrupy.assertion import SnapshotAssertion

from homeassistant.components.diagnostics import REDACTED
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from . import setup_integration

from tests.common import MockConfigEntry
from tests.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from tests.typing import ClientSessionGenerator

pytestmark = pytest.mark.usefixtures("mock_heater")

DOMAIN = "guntamatic"
SERIAL = "959103"


async def test_config_entry_diagnostics(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics have the host redacted and include data."""
    await setup_integration(hass, mock_config_entry)

    diagnostics = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert diagnostics["entry_data"][CONF_HOST] == REDACTED
    assert diagnostics == snapshot


async def test_device_diagnostics_main_device(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test main device diagnostics include all data."""
    await setup_integration(hass, mock_config_entry)

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, SERIAL), mock_config_entry.entry_id
    )
    assert device is not None

    diagnostics = await get_diagnostics_for_device(
        hass, hass_client, mock_config_entry, device
    )

    assert "boiler_temperature" in diagnostics["data"]
    assert diagnostics["entry_data"][CONF_HOST] == REDACTED


async def test_device_diagnostics_heating_circuit(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test heating circuit diagnostics only include that circuit's data."""
    await setup_integration(hass, mock_config_entry)

    device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{SERIAL}_hc1"), mock_config_entry.entry_id
    )
    assert device is not None

    diagnostics = await get_diagnostics_for_device(
        hass, hass_client, mock_config_entry, device
    )

    assert set(diagnostics["data"]) == {
        "room_1_temperature",
        "circuit_1_temp",
        "heating_circulation_pump_1",
        "heating_circulation_program_1",
    }
