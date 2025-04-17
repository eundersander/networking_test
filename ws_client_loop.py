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
                payload = f"{tag}|{i}|{send_time}"
                await websocket.send(payload)
                response = await websocket.recv()
                _, _, echo_send_time = response.split("|")
                now = time.time()
                rtt = now - float(echo_send_time)
                print(f"Client round-trip {tag} [{i}]: {rtt:.6f} s")

asyncio.run(main())
