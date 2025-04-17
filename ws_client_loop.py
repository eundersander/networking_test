# ws_client_loop.py
import asyncio
import websockets

async def main():
    uri = "ws://your-public-ip:5080"  # Replace with your server's IP
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server.")
        while True:
            msg = input("Send: ")
            if msg.lower() in ("exit", "quit"):
                print("Closing connection.")
                break
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(main())
