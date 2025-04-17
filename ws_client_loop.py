# ws_client_loop.py
import asyncio
import websockets
import time
import sys

if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <server_ip> <port>")
    sys.exit(1)

server_ip = sys.argv[1]
port = sys.argv[2]
uri = f"ws://{server_ip}:{port}"

async def main():
    async with websockets.connect(uri) as websocket:
        print(f"Connected to WebSocket server at {uri}")
        while True:
            msg = input("Enter message to test latency (or 'exit'): ")
            if msg.lower() in ("exit", "quit"):
                break
            for i in range(10):
                tag = msg.strip()
                send_time = time.time()
                payload = f"{tag}|{i}"
                await websocket.send(payload)
                await websocket.recv()
                rtt_ms = (time.time() - send_time) * 1000
                print(f"Client round-trip {tag} [{i}]: {rtt_ms:.3f} ms")

asyncio.run(main())
