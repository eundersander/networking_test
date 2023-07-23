import asyncio
import websockets

import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def hello(uri):
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("connected!")
        # Send a message to the server
        await websocket.send("Hello Server!")
        
        # Receive a message from the server
        response = await websocket.recv()
        print(f"Received: {response}")

# The address of the WebSocket server (use "wss://" for secure websockets)
uri = "wss://192.168.4.26:8888"
asyncio.get_event_loop().run_until_complete(hello(uri))