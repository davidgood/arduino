import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)