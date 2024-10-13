import asyncio
import csv
import struct
import signal
from bleak import BleakClient, BleakScanner

DEVICE_ADDRESS = None

# UUIDs for the IMU characteristics
ACC_X_CHAR_UUID = "2A37"
ACC_Y_CHAR_UUID = "2A38"
ACC_Z_CHAR_UUID = "2A39"

# CSV file setup
csv_filename = 'imu_data.csv'
running = True

# Signal handler for clean exit
def signal_handler(sig, frame):
    global running
    running = False
    print("\nExiting...")

async def find_device():
    global DEVICE_ADDRESS
    devices = await BleakScanner.discover()
    for device in devices:
        if "Nano 33 BLE IMU" in device.name or "Arduino" in device.name:
            DEVICE_ADDRESS = device.address
            print(f"Found device: {device.name} at {DEVICE_ADDRESS}")
            break

async def read_imu_data(address):
    global running
    async with BleakClient(address) as client:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['acc_x', 'acc_y', 'acc_z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            print(f"Connected to {address}. Collecting IMU data...")

            while running:
                try:
                    acc_x_bytes = await client.read_gatt_char(ACC_X_CHAR_UUID)
                    acc_y_bytes = await client.read_gatt_char(ACC_Y_CHAR_UUID)
                    acc_z_bytes = await client.read_gatt_char(ACC_Z_CHAR_UUID)

                    acc_x = struct.unpack('f', acc_x_bytes)[0]
                    acc_y = struct.unpack('f', acc_y_bytes)[0]
                    acc_z = struct.unpack('f', acc_z_bytes)[0]

                    print(f"Acc X: {acc_x}, Acc Y: {acc_y}, Acc Z: {acc_z}")
                    writer.writerow({'acc_x': acc_x, 'acc_y': acc_y, 'acc_z': acc_z})
                    csvfile.flush()

                    await asyncio.sleep(0.1)

                except Exception as e:
                    print(f"Error reading IMU data: {e}")
                    break

async def main():
    await find_device()
    if DEVICE_ADDRESS is not None:
        await read_imu_data(DEVICE_ADDRESS)
    else:
        print("No suitable BLE device found.")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    asyncio.run(main())
