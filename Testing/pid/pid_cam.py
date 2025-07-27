# DONT FORGET TO STARTTHE HOST
# RUN THIS NEXT LINE IN A SEPERATE TERMINAL
# sudo docker run -it -p 9001:9001 roboflow/roboflow-inference-server-cpu

import matplotlib.pyplot as plt
import numpy as np
from pid_log import *

from inference_sdk import InferenceHTTPClient
import cv2
import time



# set up inference
client = InferenceHTTPClient(
    api_url="http://localhost:9001", # use local inference server
    api_key="Lw0LcAJ8WMWM4TKlD71v"
)

# combine images into one to detect
def combine(frame):
	# Assume the frame contains the left and right images side by side
	height, width, _ = frame.shape
	half_width = width // 2

	# Split the image into left and right images
	left_image = frame[:, :half_width]
	right_image = frame[:, half_width:]

	# Create a combined image by overlaying (use blending or addWeighted)
	# Adjust alpha values to see both images
	alpha = 0.5  # Transparency factor
	combined_image = cv2.addWeighted(left_image, alpha, right_image, 1 - alpha, 0)
	
	return combined_image


def infer(combined_image):
	result = client.run_workflow(
	    workspace_name="bouy-detector",
	    workflow_id="detect-and-classify",
	    images={
		"image": combined_image
	    }
	)
	return result


# function that prints out objects
def detect(result, goal):
	# result is a weird object that combines lists and dictionaries
	if result and "output" in result[0]:
		output = result[0]["output"]
		predictions_data = output.get("predictions", {})
		predictions = predictions_data.get("predictions", [])
		
		# this can be used if you need to see what the variable options are
		# print(result[0])
	    
	    	# prints out every object that is detected
	    	# will look for just one in competition
		if predictions:
			for pred in predictions:
				# can include & pred["confidence"] > 0.7 or something in if statement
				if pred["class"] == goal:
					obj_cen_x = pred["x"]
					obj_cen_y = pred["y"]
					obj_w = pred["width"]
					obj_h = pred["height"]
				
				else:
					print(f"No '{goal}' found in result.")
					obj_cen_x = "none"
					obj_cen_y = "none"
					obj_w = "none"
					obj_h = "none"
		else:
			print(f"No predictions found in result.")
			obj_cen_x = "none"
			obj_cen_y = "none"
			obj_w = "none"
			obj_h = "none"
	else:
		print("No 'output' found in result.")
		obj_cen_x = "none"
		obj_cen_y = "none"
		obj_w = "none"
		obj_h = "none"
	# print()	# give a blank line to seperate each image
	return obj_cen_x, obj_cen_y, obj_w, obj_h


# PID to center horizontally
cam = cv2.VideoCapture(0)
center = 672/2
obj_cen_x = 0
"""
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, desire=center)
while obj_cen_x != center:
	# read camera each time
	info, image = cam.read(0)
	combined_image = combine(image)
	result = infer(combined_image)
	obj_cen_x, obj_cen_y, obj_w, obj_h = detect(result, "buoy")
	
	dt = 0.5
	center_out = pid.compute(obj_cen_x, dt)
	time.sleep(0.5)
"""
# PID to get closer
width = 300
obj_w = 0
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, desire=width)
while obj_w != width:
	#read camera each time
	info, image = cam.read(0)
	try:
		combined_image = combine(image)
		result = infer(combined_image)
		obj_cen_x, obj_cen_y, obj_w, obj_h = detect(result, "buoy")
		print(f"obj_w = {obj_w}")
		
		dt = 0.5
		width_out = pid.compute(obj_w, dt)
		time.sleep(0.5)
	except TypeError:
		print("no detection")
