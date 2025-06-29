import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import cv2
from cam import cam_setup, infer  # from cam.py functions

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(String, 'camera_data', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # every 1 second

        # Initialize camera and model once
        self.camera, self.model = cam_setup()

    def timer_callback(self):
        ret, frame = self.camera.read()
        if not ret:
            self.get_logger().warn("Failed to read from camera.")
            return

        results = infer(frame, self.model)

        if results and hasattr(results[0], 'predictions'):
            predictions = results[0].predictions
            json_payload = []
            for pred in predictions:
                try:
                    json_payload.append({
                        'class': pred.class_name,
                        'x': pred.x,
                        'y': pred.y,
                        'width': pred.width,
                        'height': pred.height,
                        'confidence': pred.confidence
                    })
                except AttributeError:
                    self.get_logger().warn("Missing expected prediction fields.")
                    continue

            msg = String()
            msg.data = json.dumps(json_payload)
            self.publisher_.publish(msg)
            self.get_logger().info(f"Published {len(json_payload)} objects.")
        else:
            self.get_logger().info("No objects detected.")

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
