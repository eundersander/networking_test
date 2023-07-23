
import math

num_cubes = 20
max_step_rate = 1.0 / 100

from server_websockets import launch_server_process
from interprocess_record import send_keyframe_to_networking_thread

from frequency_limiter import FrequencyLimiter
  

def run_sim():

    launch_server_process()

    # Define circle parameters
    center_x = 0
    center_z = 0
    radius = 2
    dt = 1 / 10
    angular_inc = math.pi * 2 * 0.1 * dt

    angular_offset = 2 * math.pi / num_cubes
    base_angle = 0
    step_count = 0

    frequency_limiter = FrequencyLimiter(2.0)

    # move cubes in a circle over time
    while True:

        cube_poses = []
        for i in range(num_cubes):
            # Calculate the angle for each cube
            angle = base_angle + i * angular_offset

            # Calculate cube position in the circle
            cube_x = center_x + radius * math.cos(angle)
            cube_y = 1 + i * 0.1  # Different Y height for each cube
            cube_z = center_z + radius * math.sin(angle)

            # Update cube pose
            cube_pose = {
                "rotation": {"x": 0, "y": 0, "z": 0, "w": 1},
                "translation": {"x": cube_x, "y": cube_y, "z": cube_z}
            }
            cube_poses.append(cube_pose)

        keyframe = {"keyframe_index": step_count, "cube_poses": cube_poses}

        # Update the angles for the next iteration
        base_angle += angular_inc

        send_keyframe_to_networking_thread(keyframe)

        frequency_limiter.limit_frequency()

        step_count += 1
        if step_count % 10 == 0:
            print(f"step_count: {step_count}")

if __name__ == "__main__":
    run_sim()
