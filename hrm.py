import asyncio
from bleak import BleakClient
from DB import save_heart_rate, save_home_heartbeats_count

DEVICE_ADDRESS = "C1:A3:55:84:E6:53"
HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
USER_ID = 1  # Fix for test

async def connect_to_device():
    current_bpm = None
    bpm_count = 0

    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected to Garmin HRM Dual")

        if not client.is_connected:
            print("Device is not connected properly!")
            return

        services = client.services 
        
        if HEART_RATE_UUID not in [char.uuid for service in services for char in service.characteristics]:
            print("Heart Rate characteristic not found!")
            return

        def heart_rate_handler(sender, data):
            nonlocal current_bpm, bpm_count
            bpm = data[1]
            print(f"Received heart rate: {bpm}")

            if current_bpm is None:
                current_bpm = bpm
                bpm_count = 1
            elif bpm == current_bpm:
                bpm_count += 1
            else:
                # Beat changes
                # Save new beat in home_heartbeats
                rate_id = save_heart_rate(USER_ID, current_bpm, tag_no="garmin_hrm", description="Heart rate from Garmin")
                # Save count of beat in home_heartbeats_count
                save_home_heartbeats_count(rate_id, bpm_count)

                # New BPM
                current_bpm = bpm
                bpm_count = 1

        await client.start_notify(HEART_RATE_UUID, heart_rate_handler)

        try:
            await asyncio.sleep(10)  # Monitor time
        finally:
            # Save last BPM when time over
            if bpm_count > 0:
                rate_id = save_heart_rate(USER_ID, current_bpm, tag_no="garmin_hrm", description="Heart rate from Garmin")
                save_home_heartbeats_count(rate_id, bpm_count)

            await client.stop_notify(HEART_RATE_UUID)

if __name__ == "__main__":
    asyncio.run(connect_to_device())
