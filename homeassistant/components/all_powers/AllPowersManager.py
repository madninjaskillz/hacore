"""Allpowers manager service."""
import asyncio

from bleak import BleakClient, BleakScanner

from . import AllPowersData


class AllPowersManagerService:
    """Allpowers manager service."""

    all_powers_data: AllPowersData.AllPowersData

    def notification_handler(self, data):
        """Allpowers notification handler."""
        self.all_powers_data.battery_percentage = data[8]
        self.all_powers_data.dc_on = data[7] >> 0 & 1 == 1
        self.all_powers_data.ac_on = data[7] >> 1 & 1 == 1
        self.all_powers_data.torch_on = data[7] >> 4 & 1 == 1
        self.all_powers_data.output_power = (256 * data[11]) + data[12]
        self.all_powers_data.input_power = (256 * data[9]) + data[10]
        self.all_powers_data.minutes_remaining = (256 * data[13]) + data[14]

    def set_bit(self, v: int, index: int, x: bool) -> int:
        """Set bit."""
        return_value: int
        return_value = v
        mask = 1 << index
        if x:
            return_value |= mask
        else:
            return_value &= ~mask
        return return_value

    async def change_status_to_device(
        self, client: BleakClient, xdata: AllPowersData.AllPowersData
    ):
        """Send datamodel back to Allpowers."""
        full = bytes.fromhex("a56500b10101000071")
        s = bytearray(9)
        for x in range(9):
            s[x] = full[x]

        s[7] = 0
        s[7] = AllPowersManagerService.set_bit(self, s[7], 5, xdata.torch_on)
        s[7] = AllPowersManagerService.set_bit(self, s[7], 0, xdata.dc_on)
        s[7] = AllPowersManagerService.set_bit(self, s[7], 1, xdata.ac_on)

        s[8] = 113 - s[7]
        if xdata.ac_on:
            s[8] = s[8] + 4

        await client.write_gatt_char("0000FFF2-0000-1000-8000-00805F9B34FB", s)

    def getData(self):
        """Get Allpowers data model."""
        return self.all_powers_data

    async def main(self):
        """Allpowers service runner."""
        self.all_powers_data = AllPowersData.AllPowersData()
        my_device = None
        while my_device is None:
            devices = await BleakScanner.discover()
            for d in devices:
                if d.name is not None:
                    if d.name == "AP S300 V2.0":
                        my_device = d
                        async with BleakClient(my_device.address) as client:
                            for service in client.services:
                                for char in service.characteristics:
                                    if "notify" in char.properties:
                                        await client.start_notify(
                                            char,
                                            AllPowersManagerService.notification_handler,
                                        )
            await asyncio.sleep(1)
