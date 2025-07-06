# DONT FORGET TO STARTTHE HOST
# RUN THIS NEXT LINE IN A SEPERATE TERMINAL
# sudo docker run -it -p 9001:9001 roboflow/roboflow-inference-server-cpu


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

	
	
def nav_obj(x,y,c_w, c_h, bound):
	mid = c_w / 2
	left_mid = mid - bound
	right_mid = mid + bound
	
	if x == "none":
		print("R")	# turn to find object, may need to go forward as well
	elif x < left_mid:
		print("R")
	elif x > right_mid:
		print("L")
	else:
		print("S")
	
		
		

#camera
cam = cv2.VideoCapture(0)
cam_height = 376
cam_width = 672
cam_bound = 20


# get result in real time
while True:
	info, image = cam.read(0)
	combined_image = combine(image)
	result = infer(combined_image)
	obj_cen_x, obj_cen_y, obj_w, obj_h = detect(result, "buoy")
	nav_obj(obj_cen_x, obj_cen_y, cam_width, cam_height, cam_bound)
	print(obj_cen_x, obj_cen_y, obj_w, obj_h)
	print()
	time.sleep(1)
	
    

