# relay_client.py
import socketio
import sys

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <server_ip>")
    sys.exit(1)

server_ip = sys.argv[1]
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server.")

@sio.event
def message(data):
    print(f"> {data}")
    if "you go first" in data.lower() or "peer connected" in data.lower():
        interact()

@sio.event
def disconnect():
    print("Disconnected from server.")

def interact():
    while True:
        msg = input("You: ")
        if msg.lower() in ('exit', 'quit'):
            sio.disconnect()
            break
        sio.send(msg)

sio.connect(f"http://{server_ip}:37064")
sio.wait()
