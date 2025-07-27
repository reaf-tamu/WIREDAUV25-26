# run this in terminal
# source install/setup.bash

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
import time
import threading
import json

from logic.vn_log import check_vn
from logic.cam_log import detect, nav_obj

class Listener(Node):
	def __init__(self):
		super().__init__('listener')
		
		self.vn_sub = self.create_subscription(
			Float32,
			'vn',
			self.vn_data,
			10)
			
		self.ms_sub = self.create_subscription(
			Bool,
			'ms',
			self.ms_data,
			10)
			
		self.cam_sub = self.create_subscription(
			String,
			'camera_data',
			self.cam_data,
			10)
			
		self.vn_x = None
		self.ms = None
		self.cam_res = None

	def vn_data(self, msg):
		self.vn_x = msg.data
		
	def ms_data(self, msg):
		self.ms = msg.data
		
	def cam_data(self, msg):
		self.cam_res = msg.data
	def get_cam(self):
		return self.cam_res

	def get_data(self):
		return self.vn_x, self.ms
		
	





def main(args=None):
	rclpy.init(args=args)
	sub = Listener()
	
	
	# runs rclpy.spin
	ros_thread = threading.Thread(target=rclpy.spin, args=(sub,), daemon=True)
	ros_thread.start()
	time.sleep(3)
	
	
	vn_x, ms = sub.get_data()
	print(ms)
	
	# wait for missin switch to activate
	print("Mission switch activating…")
	print(ms)
	while (ms == False):
		print(ms)
		vn_x, ms = sub.get_data()
		time.sleep(0.1)
	print("Beginning code in 3 seconds")
	time.sleep(3)
	
	
	# begin  loop
	count = 0
	while True:
		# vectornav origin , taking 5 samples and averaging
		headings = []
		for i in range(5):
			heading, ms = sub.get_data()
			if heading is not None:
				headings.append(heading)
				time.sleep(0.5)
		origin = sum(headings) / len(headings)
		print(f'Origin = {origin}')
	
		# main loop
		vn_x, ms = sub.get_data()
		while ms == False:
			#print(count, ms)
			#count += 1
			vn_x, ms = sub.get_data()
			
			
			# maintain heading using vectornav
			check_vn(vn_x, origin, 10)
			
			# get result from pub and unstring
			result_str = sub.get_cam()
			
			result = json.loads(result_str)
			# look for buoy
			obj_cen_x, obj_cen_y, obj_w, obj_h = detect(result, "buoy")
			# nav_obj(obj_cen_x, obj_cen_y, bound = 20)
			print(obj_cen_x, obj_cen_y, obj_w, obj_h)
			print()

	
			
			
			time.sleep(0.5)
		
		
		
		
		
		
		
		
		
		# stops code after first press
		print("stopping code")
		time.sleep(3)	
		count = 0
		
		# waiting loop, press button again to restart
		vn_x, ms = sub.get_data()
		while (ms == False):
			print(ms)
			vn_x, ms = sub.get_data()
			time.sleep(0.1)
		
		print("restarting code in 3 seconds")
		time.sleep(3)

	# Destroy the node explicitly
	sub.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()
