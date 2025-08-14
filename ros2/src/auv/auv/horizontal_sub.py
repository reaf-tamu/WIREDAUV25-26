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
  def get_data(self):
		return self.vn_x, self.ms
		
	def cam_data(self, msg):
		self.cam_res = msg.data
	def get_cam(self):
		return self.cam_res





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
	while True:
    # main loop
		vn_x, ms = sub.get_data()
		while ms == False:
			# get camera from pub and unstring
			result_str = sub.get_cam()
			result = json.loads(result_str)
			
			# look for gate middle and right
			gm_cen_x, gm_cen_y, gm_w, gm_h = detect(result, "gate_m")
			gr_cen_x, gr_cen_y, gr_w, gr_h = detect(result, "gate_r")

			# if neither object is detected, spin
			# elif only gm is detected, move to the right
			# elif only gr is detected, move to the left
			# elif/else both are detected, more logic
				# navigate to center between objects using cen_x values
				# save heading as vn origin
				# use vectornav to go straight using this logic
				check_vn(vn_x, origin, 10)
				# if not centered, it needs to restart this indented section
			# when it no longer detects gate bc it is passing it, have it go straight for a few seconds longer to pass under
			
			# we will use similar logic for slaloms
			# wait to code this until we know it works for gate
			
			

			
			# last line of main loop
			vn_x, ms = sub.get_data() # checks mission switch status at end of loop
			time.sleep (0.5)
		

		
		
		# stops code after first press
		print("stopping code")
		time.sleep(3)	
		count = 0
		
		# waiting loop, press button again to restart
		ping, ms = sub.get_data()
		while (ms == False):
			print(ms)
			ping, ms = sub.get_data()
			time.sleep(0.1)
		
		print("restarting code in 3 seconds")
		time.sleep(3)

	# Destroy the node explicitly
	sub.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()

