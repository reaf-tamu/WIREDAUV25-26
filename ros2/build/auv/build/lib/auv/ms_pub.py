import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import Jetson.GPIO as GPIO
import time

PIN = 32  #change if needed (based on tanvi k’s code)
class MissionSwitchPublisher(Node):
    def __init__(self):
        super().__init__('mission_switch_publisher')
        self.publisher_ = self.create_publisher(Bool, 'ms', 10)

        # GPIO setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.IN)

        self.timer = self.create_timer(0.1, self.timer_callback)  # 100ms timer

    def timer_callback(self):
        raw_state = GPIO.input(PIN)
        state = (raw_state == GPIO.HIGH)  # True when button is released
        msg = Bool()
        msg.data = state
        self.get_logger().info(f"Publishing Mission Switch State: {msg.data}")
        self.publisher_.publish(msg)

    def destroy_node(self):
        super().destroy_node()
        GPIO.cleanup()  # Clean up GPIO on shutdown


def main(args=None):
    rclpy.init(args=args)
    node = MissionSwitchPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
