# pid_cam.py

import time
import numpy as np
from inference_sdk import InferenceHTTPClient
from pid_log import PIDController
import pyzed.sl as sl
import cv2

# ---------------------- Inference Setup ----------------------

client = InferenceHTTPClient(
    api_url="http://localhost:9001",  # Roboflow inference server
    api_key="Lw0LcAJ8WMWM4TKlD71v"
)

# ---------------------- ZED Camera Setup ----------------------

zed = sl.Camera()

init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.VGA  # 672x376
init_params.camera_fps = 30

err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print(f"ZED camera open failed: {err}")
    exit(1)

runtime = sl.RuntimeParameters()
image = sl.Mat()

# ---------------------- Helper Functions ----------------------

def infer(image_np):
    """Run inference on the input image (numpy array)"""
    result = client.run_workflow(
        workspace_name="bouy-detector",
        workflow_id="detect-and-classify",
        images={"image": image_np}
    )
    return result

def detect(result, goal):
    """Extract object info for a given class name"""
    if result and "output" in result[0]:
        predictions_data = result[0]["output"].get("predictions", {})
        predictions = predictions_data.get("predictions", [])
        for pred in predictions:
            if pred["class"] == goal:
                return pred["x"], pred["y"], pred["width"], pred["height"]
        print(f"No '{goal}' found in result.")
    else:
        print("Invalid result format or no output.")
    return None, None, None, None

# ---------------------- PID Controller ----------------------

target_width = 400  # Desired object width in pixels
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, desire=target_width)

# ---------------------- Main Loop ----------------------

try:
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.SIDE_BY_SIDE)
            frame = image.get_data()

            # frame shape: (376, 672, 4) — includes alpha, drop to 3 channels if needed
            frame_rgb = frame[:, :, :3].copy()  # Drop alpha if present

            result = infer(frame_rgb)
            obj_cen_x, obj_cen_y, obj_w, obj_h = detect(result, "buoy")

            if obj_w is not None and obj_w != "none":
                print(f"Detected buoy width: {obj_w}")
                dt = 0.5
                width_out = pid.compute(obj_w, dt)
                print(f"PID output: {width_out}")
                time.sleep(dt)
            else:
                print("No buoy detected.")
                time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    zed.close()

