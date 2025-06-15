import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from vnpy import *

# connect sensor
s = VnSensor()	# saves VN object to variable s
s.connect("/dev/ttyUSB0",115200)	# connects to VN at USB0, baud rate 115200


class Talker(Node):		# sets up publisher as talker
	def __init__(self):			# publisher name chatter
		super().__init__('talker')
		self.publisher_ = self.create_publisher(Float32, 'vn', 10)
		self.timer = self.create_timer(0.5, self.timer_callback)  # sleeps for 0.1 seconds

	def timer_callback(self):		# sets up message to be published
		orientation = s.read_yaw_pitch_roll()
		x = orientation.x
		message = Float32()
		message.data = x
		self.get_logger().info(f"Heading x = {message.data}")
		self.publisher_.publish(message)
def main(args=None):
	rclpy.init(args=args)
	node = Talker()
	try:
		rclpy.spin(node) #like a while loop 
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()

if __name__ == '__main__':
	main()


