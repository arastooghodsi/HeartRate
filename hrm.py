import asyncio
from bleak import BleakClient
from DB import save_heart_rate

DEVICE_ADDRESS = "C1:A3:55:84:E6:53"  # Enter your device address.
HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
USER_ID = 1  # For testing, I'll set a fixed user_id. You can change it.

async def connect_to_device():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected to Garmin HRM Dual")

        def heart_rate_handler(sender, data):
            bpm = data[1]
            print(f"Heart rate: {bpm}")
            save_heart_rate(USER_ID, bpm, tag_no="garmin_hrm", description="Heart rate from Garmin")

        await client.start_notify(HEART_RATE_UUID, heart_rate_handler)
        await asyncio.sleep(60)
        await client.stop_notify(HEART_RATE_UUID)

if __name__ == "__main__":
    asyncio.run(connect_to_device())