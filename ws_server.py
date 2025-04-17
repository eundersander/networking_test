# ws_server.py
import asyncio
import websockets
import time

async def handler(websocket):
    print("Client connected.")
    prev_recv = None
    while True:
        message = await websocket.recv()
        now = time.time()
        if prev_recv is not None:
            interval_ms = (now - prev_recv) * 1000
            print(f"Server round-trip interval: {interval_ms:.3f} ms")
        prev_recv = now
        await websocket.send(message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 5080):
        print("WebSocket server listening on port 5080...")
        await asyncio.Future()  # Run forever

asyncio.run(main())
