# DONT FORGET TO STARTTHE HOST
# RUN THIS NEXT LINE IN A SEPERATE TERMINAL
# sudo docker run -it -p 9001:9001 roboflow/roboflow-inference-server-cpu

# logic/cam_log.py

import cv2

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
	

	
def infer(combined_image, client):
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
					obj_cen_x = obj_cen_y = obj_w = obj_h = None

		else:
			print(f"No predictions found in result.")
			obj_cen_x = obj_cen_y = obj_w = obj_h = None
	else:
		print("No 'output' found in result.")
		obj_cen_x = obj_cen_y = obj_w = obj_h = None
	# print()	# give a blank line to seperate each image
	return obj_cen_x, obj_cen_y, obj_w, obj_h

	
cam_height = 376
cam_width = 672
cam_bound = 20

	
	
def nav_obj(x,y, bound, c_h = 376, c_w = 672):
	mid = c_w / 2
	left_mid = mid - bound
	right_mid = mid + bound
	
	if x < left_mid:
		print("R")
	elif x > right_mid:
		print("L")
	else:
		print("S")

def between_obj(mx, rx, bound):
	# neither is detected, spin
	if ((mx == None) and (rx == None)):
		motion = "R"
	# only middle detected, turn right
	elif ((mx != None) and (rx == None)):
		motion = "R"
	# only right detect, turn left
	elif ((mx == None) and (rx != None)):
		motion = "L"
	# both are detected
	else:
		target = (mx + rx) / 2.0
		left_mid = (672/2) - bound
		right_mid = (672/2) + bound

		# stay within center bound
		if x < left_mid:
			motion = "R"
		elif x > right_mid:
			motion = "L"
		else:
			motion = "vn"
	
	return motion
