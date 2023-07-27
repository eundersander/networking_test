This readme is incomplete; ask Eric if you run into issues.

# server_websockets.py

This should be used in the SIRo HITL tool or another simulation. The relevant API is:
```
from server_websockets import launch_server_process, terminate_server_process
from interprocess_record import send_keyframe_to_networking_thread, get_queued_client_states
```
Concretely, to work with vrcube.html, the simulation thread should send keyframes consisting of poses for the set of cubes expected by `client_vrcube.js`.

It requires `self_signed.pem` and `private.key`, which you can generate with [these instructions](https://docs.google.com/document/d/1hXuStZKNJafxLQVgl2zy2kyEf8Nke-bYogaPuHYT_M4/edit#bookmark=id.jva9nto0xpbe).

# vrcube.html

This is a minimal WebXR client app. It should be served via HTTPS (including related `.js` files in this folder); see [these instructions](https://docs.google.com/document/d/1hXuStZKNJafxLQVgl2zy2kyEf8Nke-bYogaPuHYT_M4/edit#bookmark=id.jva9nto0xpbe). It'll connect to the server, receive keyframes, use them to update the poses of some cubes, and also send updated "client state" (keyboard state; VR controller poses and button states).

`mouseKeyboardAvatar.js` is misnamed; it's an avatar that is controlled by the keyboard when in desktop mode or controlled by VR when in VR mode.
