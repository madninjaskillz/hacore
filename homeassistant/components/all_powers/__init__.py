"""The All Powers S300 integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from . import AllPowersManager
from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up All Powers S300 from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    allPowersManager: AllPowersManager.AllPowersManagerService
    allPowersManager = AllPowersManager.AllPowersManagerService()
    await allPowersManager.main()
    hass.data[DOMAIN][entry.entry_id] = allPowersManager
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
