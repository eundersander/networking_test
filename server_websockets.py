import asyncio
import websockets
import ssl
import json
import threading

import multiprocessing_config
from frequency_limiter import FrequencyLimiter
from interprocess_record import interprocess_record, send_client_state_to_main_thread, get_queued_keyframes

# Boolean variable to indicate whether to use SSL
use_ssl = True

server_process = None
exit_event = None

def launch_server_process():
    # see multiprocessing_config to switch between real and dummy multiprocessing

    global server_process
    global exit_event

    # multiprocessing.dummy.Process is actually a thread and requires special logic
    # to terminate it.
    exit_event = threading.Event() if multiprocessing_config.use_dummy else None

    server_process = multiprocessing_config.Process(target=server_main, args=(interprocess_record, exit_event))
    server_process.start()  

def terminate_server_process():
    global server_process
    global exit_event
    if multiprocessing_config.use_dummy:
        if exit_event:
            exit_event.set()
            exit_event = None
    else:
        if server_process:
            server_process.terminate()
            server_process = None

def create_ssl_context():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='../networking_test/self_signed.pem', keyfile='../networking_test/private.key')
    return ssl_context

class Server:

    def __init__(self, interprocess_record, exit_event):

        self._connected_clients = {}  # Dictionary to store connected clients

        # todo: get rid of this if not needed (we're currently using a global)
        self._interprocess_record = interprocess_record

        # Limit how many messages/sec we send. Note the current server implementation sends
        # messages "one at a time" (waiting for confirmation of receipt from the
        # remote client OS), so there is probably no risk of overwhelming the
        # network connection bandwidth even when sending at a high rate.
        max_send_rate = None  # or set None to not limit
        self._send_frequency_limiter = FrequencyLimiter(max_send_rate) 

        self._exit_event = exit_event

    async def send_keyframes(self, websocket):

        while True:

            if self._exit_event and self._exit_event.is_set():
                break

            # todo: refactor to support N clients
            keyframes = get_queued_keyframes()

            if len(keyframes):
                # Convert keyframes to JSON string
                keyframes_json = json.dumps(keyframes)

                # Send cube poses to the client
                keyframe_index = keyframes[-1]["keyframe_index"]
                # if keyframe_index % 10 == 0:  # sloppy, we miss a lot of frames
                #     print(f"sending keyframe {keyframe_index}")
                # print(f"mock sending keyframes_json: {keyframes_json}")
                
                # note this awaits until the client OS has received the message
                await websocket.send(keyframes_json)

                # limit how often we send
                await self._send_frequency_limiter.limit_frequency_async()

            else:
                await asyncio.sleep(0.02)  # todo: think about how best to do this

            # todo: don't send a message more often than 1.0 / maxSendRate

            # todo: don't busy loop here

    async def receive_avatar_pose(self, websocket):
        async for message in websocket:
            try:
                # Parse the received message as a JSON object
                client_state = json.loads(message)

                send_client_state_to_main_thread(client_state)

            except json.JSONDecodeError:
                print("Received invalid JSON data from the client.")
            except KeyError as e:
                print(f"Missing key '{e.args[0]}' in the received JSON data.")
            except Exception as e:
                print(f"Error processing received pose data: {e}")


    async def serve(self, websocket):
        # Store the client connection object in the dictionary
        self._connected_clients[id(websocket)] = websocket

        if self._exit_event and self._exit_event.is_set():
            await websocket.close()  # not sure if this is correct
            return

        try:
            print(f"waiting for message from client {id(websocket)}")
            message = await websocket.recv()

            if message == "vrcube client ready":
                # await self.send_keyframes(websocket)

                # Start the tasks concurrently using asyncio.gather
                await asyncio.gather(
                    self.send_keyframes(websocket),
                    self.receive_avatar_pose(websocket)
                )                

            else:
                raise RuntimeError(f"unexpected message from client: {message}")

        finally:
            # Remove the client connection from the dictionary when it disconnects
            del self._connected_clients[id(websocket)]
        
def server_main(interprocess_record, exit_event):

    global use_ssl

    if multiprocessing_config.use_dummy:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    server_obj = Server(interprocess_record, exit_event)
    server_lambda = lambda ws, path: server_obj.serve(ws)
    ssl_context = create_ssl_context() if use_ssl else None     
    start_server = websockets.serve(server_lambda, "0.0.0.0", 8888, ssl=ssl_context)
    # start_server = websockets.serve(server_lambda, "0.0.0.0", 8888)

    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started. Waiting for clients...")
    while not (exit_event and exit_event.is_set()):
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(1.0))  # todo: investigate what sleep duration does here

    print("server_main finished")