# run this in terminal
# source install/setup.bash

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
import time
import threading
import json

from logic.ping_log import check_depth

class Listener(Node):
	def __init__(self):
		super().__init__('listener')
		
		self.ping_sub = self.create_subscription(
			Float32,
			'ping',
			self.ping_data,
			10)
			
		self.ms_sub = self.create_subscription(
			Bool,
			'ms',
			self.ms_data,
			10)
			
			
		self.ping = None
		self.ms = None

	def ping_data(self, msg):
		self.ping = msg.data
		
	def ms_data(self, msg):
		self.ms = msg.data

	def get_data(self):
		return self.ping, self.ms



def main(args=None):
	rclpy.init(args=args)
	sub = Listener()
		
	# runs rclpy.spin
	ros_thread = threading.Thread(target=rclpy.spin, args=(sub,), daemon=True)
	ros_thread.start()
	time.sleep(3)
	
	
	ping, ms = sub.get_data()
	print(ms)
	
	# wait for missin switch to activate
	print("Mission switch activating…")
	print(ms)
	while (ms == False):
		print(ms)
		ping, ms = sub.get_data()
		time.sleep(0.1)
	print("Beginning code in 3 seconds")
	time.sleep(3)
	
	
	# begin  loop
	while True:
    # main loop
		ping, ms = sub.get_data()
		while ms == False:
			ping, ms = sub.get_data()
			
			# get result from pub and unstring
      		# will I need to do this for pinger?
			# result_str = sub.get_cam()
			# result = json.loads(result_str)

     		# maintain depth
      		check_depth(16, 1, ping)
			time.sleep(0.5)
		
		
	
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
