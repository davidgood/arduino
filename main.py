import asyncio
import csv
import struct
from os import write

from bleak import BleakClient

# Replace this with your Arduino's BLE address (use the scanner script to find it)
#DEVICE_ADDRESS = "BE19FF27-3666-1FE8-1486-E6E19B81BEB0"
DEVICE_ADDRESS = "9F810906-539E-E2DD-4CA8-A71757F0AA24"

# UUIDs for the IMU characteristics
ACC_X_CHAR_UUID = "2A37"
ACC_Y_CHAR_UUID = "2A38"
ACC_Z_CHAR_UUID = "2A39"

# CSV file setup
csv_filename = 'imu_data.csv'

# Function to connect and read IMU data
async def read_imu_data(address):
    async with BleakClient(address) as client:
        # Open the CSV file and prepare to write the data
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['acc_x', 'acc_y', 'acc_z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write header to the CSV

            print(f"Connected to {address}. Collecting IMU data...")

            while True:
                try:
                    # Read the accelerometer data from the BLE device
                    acc_x_bytes = await client.read_gatt_char(ACC_X_CHAR_UUID)
                    acc_y_bytes = await client.read_gatt_char(ACC_Y_CHAR_UUID)
                    acc_z_bytes = await client.read_gatt_char(ACC_Z_CHAR_UUID)

                    # Convert byte data to float using struct.unpack
                    acc_x = struct.unpack('f', acc_x_bytes)[0]
                    acc_y = struct.unpack('f', acc_y_bytes)[0]
                    acc_z = struct.unpack('f', acc_z_bytes)[0]

                    # Print the IMU data to the console
                    print(f"Acc X: {acc_x}, Acc Y: {acc_y}, Acc Z: {acc_z}")

                    # Write the IMU data to the CSV file
                    writer.writerow({'acc_x': acc_x, 'acc_y': acc_y, 'acc_z': acc_z})
                    writer.flush()

                    # Wait before the next reading
                    await asyncio.sleep(0.1)

                except Exception as e:
                    print(f"Error reading IMU data: {e}")
                    break

# For Python 3.10 and later: Create new event loop explicitly
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(read_imu_data(DEVICE_ADDRESS))