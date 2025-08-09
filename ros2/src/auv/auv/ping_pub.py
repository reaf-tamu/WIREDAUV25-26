import rclpy 	 	# ROS2 rospy
from rclpy.node import Node
from std_msgs.msg import Float32		# data type is float value
from burping import Ping1D			# pinger module

# connect to pinger
myPing = Ping1D()
myPing.connect_serial("/dev/ttyUSB1", 115200)
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)
myPing.set_ping_interval(29)
myPing.set_speed_of_sound(1500)


class Pinger(Node):	# sets up publisher as talker
    def __init__(self):			# publisher name chatter
        super().__init__('pinger_publisher')
        self.publisher_ = self.create_publisher(String, 'ping_sub', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # sleeps for 0.1 seconds

    def timer_callback(self):		# sets up message to be published
       data = myPing.get_distance_simple()	# get measured values
       message = Float32()			# sets message type
       message.data = data['distance']		# saves depth value to message
       self.get_logger().info(f"Publishing Distance: {message.data}")
       self.publisher_.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
