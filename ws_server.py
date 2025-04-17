# ws_server.py
import asyncio
import websockets
import time

async def handler(websocket):
    while True:
        message = await websocket.recv()
        tag, index, send_time = message.split("|")
        now = time.time()
        rtt = now - float(send_time)
        print(f"Server round-trip {tag} [{index}]: {rtt:.6f} s")
        await websocket.send(message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 37064):
        await asyncio.Future()  # Run forever

asyncio.run(main())
