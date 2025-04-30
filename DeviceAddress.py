import asyncio
from bleak import BleakScanner

async def find_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(find_devices())