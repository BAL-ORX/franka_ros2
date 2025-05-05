import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage

class JpegSaver(Node):
    def __init__(self):
        super().__init__('jpeg_saver')
        self.latest = None

        # subscribe to the compressed JPEG topic
        self.create_subscription(
            CompressedImage,
            '/camera/camera/color/image_rect_raw/compressed',
            self.cb_compressed,
            10)

        # one-shot timer: after 2 seconds, call save_and_exit()
        self.create_timer(2.0, self.save_and_exit)

    def cb_compressed(self, msg: CompressedImage):
        # store the most recent frame
        self.latest = msg

    def save_and_exit(self):
        if self.latest is None:
            self.get_logger().warn('No compressed image received yet')
            return

        # build the output folder with a space in its name
        home = os.path.expanduser('~')   # → '/home/user'
        out_dir = os.path.join(home,
                       'Bachelor Thesis',
                       'realsense_pictures')

        os.makedirs(out_dir, exist_ok=True)

        # filename with timestamp
        ts = self.get_clock().now().nanoseconds
        path = os.path.join(out_dir, f'color_{ts}.jpg')

        # dump the raw JPEG bytes
        with open(path, 'wb') as f:
            f.write(self.latest.data)

        self.get_logger().info(f'Saved JPEG to {path}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = JpegSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
