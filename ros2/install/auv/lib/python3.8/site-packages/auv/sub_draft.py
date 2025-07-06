import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
import time
import threading

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
			
		self.vn_x = None
		self.ms = None
		
		#self.create_timer(0.1, self.code)

	def vn_data(self, msg):
		self.vn_x = msg.data
		#print(self.vn_x)
		
	def ms_data(self, msg):
		self.ms = msg.data
		#print(self.ms)
		
	def get_data(self):
		return self.vn_x, self.ms
	
	"""
	def code():
		print("here?")
	
	def mission(self):
		if self.ms == True:
			code()
		else:
			print("nope")
		
	

		while (self.ms == False):
			print(self.ms)
			time.sleep(0.1)

		print("beginning code")
		time.sleep(3)

		count = 0

		while True:
			while (self.ms == False):
				print(count)
				count += 1
				print(self.vn_x)
				time.sleep(0.1)
			
			time.sleep(3)	
			print("pausing code")
			count = 0
			
			while (self.ms == False):
				print(self.ms)
				time.sleep(0.1)
			
			time.sleep(3)
			print("restarting code")
		"""


def main(args=None):
	rclpy.init(args=args)
	sub = Listener()
	
	# rclpy.spin(listener)
	ros_thread = threading.Thread(target=rclpy.spin, args=(sub,), daemon=True)
	ros_thread.start()
	

	while True:
		vn_x, ms = sub.get_data()
		
		print(vn_x, ms)
		
		time.sleep(1)

	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	sub.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()
