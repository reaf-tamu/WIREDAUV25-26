# DONT FORGET TO STARTTHE HOST
# RUN THIS NEXT LINE IN A SEPERATE TERMINAL
# sudo docker run -it -p 9001:9001 roboflow/roboflow-inference-server-cpu

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import cv2
from inference_sdk import InferenceHTTPClient

from logic.cam_log import combine, infer

cam = cv2.VideoCapture(0)

# set up inference
client = InferenceHTTPClient(
	api_url="http://localhost:9001", # use local inference server
	api_key="Lw0LcAJ8WMWM4TKlD71v"
)



class CameraPublisher(Node):
	def __init__(self):
		super().__init__('camera_publisher')
		self.publisher_ = self.create_publisher(String, 'camera_data', 10)
		self.timer = self.create_timer(0.1, self.timer_callback)  # every 1 second


	def timer_callback(self):
		info, image = cam.read(0)
		combined_image = combine(image)
		result = infer(combined_image, client)


		msg = String()
		msg.data = json.dumps(result)
		self.publisher_.publish(msg)
		self.get_logger().info(msg.data)


def main(args=None):
	rclpy.init(args=args)
	node = CameraPublisher()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()

if __name__ == '__main__':
	main()
	
	
