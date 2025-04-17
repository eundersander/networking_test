# ws_server.py
import asyncio
import websockets

async def handler(websocket):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 5080):
        await asyncio.Future()  # run forever

asyncio.run(main())
