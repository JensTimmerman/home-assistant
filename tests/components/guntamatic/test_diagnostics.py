"""Tests for the Guntamatic diagnostics."""

import pytest
from syrupy.assertion import SnapshotAssertion

from homeassistant.components.diagnostics import REDACTED
from homeassistant.core import HomeAssistant

from . import setup_integration

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator

pytestmark = pytest.mark.usefixtures("mock_heater")


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

    assert diagnostics["entry_data"]["host"] == REDACTED
    assert diagnostics == snapshot
