"""Platform for All Powers S300 integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from . import AllPowersData, AllPowersManager
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the AllPowers sensors."""
    async_add_entities(
        [
            BatteryRemainingSensor(hass.data[DOMAIN][config_entry.entry_id]),
            OutputPowerSensor(hass.data[DOMAIN][config_entry.entry_id]),
        ]
    )


class BatteryRemainingSensor(SensorEntity):
    """AllPowers S300 Battery Remaining."""

    _attr_name = "AllPowers S300 Battery Remaining"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    all_powers_manager: AllPowersManager.AllPowersManagerService

    def __init__(self, apm: AllPowersManager.AllPowersManagerService) -> None:
        """Ctor."""
        self.all_powers_manager = apm

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        data: AllPowersData.AllPowersData
        data = self.all_powers_manager.getData()
        self._attr_native_value = data.minutes_remaining


class OutputPowerSensor(SensorEntity):
    """AllPowers S300 Output Power."""

    _attr_name = "AllPowers S300 Output Power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = None
    all_powers_manager: AllPowersManager.AllPowersManagerService

    def __init__(self, apm: AllPowersManager.AllPowersManagerService) -> None:
        """Ctor."""
        self.all_powers_manager = apm

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        data: AllPowersData.AllPowersData
        data = self.all_powers_manager.getData()
        self._attr_native_value = data.output_power
