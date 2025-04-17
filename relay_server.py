# relay_server.py
import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

clients = []

@sio.event
async def connect(sid, environ):
    ip = environ.get("REMOTE_ADDR")
    print(f"Client connected: {ip} ({sid})")

    if len(clients) >= 2:
        await sio.emit('message', 'Server full.', room=sid)
        await sio.disconnect(sid)
        return

    clients.append(sid)
    idx = len(clients)
    await sio.emit('message', f"Connected as client {idx}", room=sid)

    if len(clients) == 2:
        await sio.emit('message', 'Peer connected. You go first.', room=clients[0])
        await sio.emit('message', 'Peer connected. Wait for a message...', room=clients[1])

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    for peer_sid in clients:
        if peer_sid != sid:
            await sio.emit('message', data, room=peer_sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    if sid in clients:
        clients.remove(sid)
    for peer_sid in clients:
        await sio.emit('message', 'Peer disconnected.', room=peer_sid)

if __name__ == '__main__':
    web.run_app(app, port=37064)
