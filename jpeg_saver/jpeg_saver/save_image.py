import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage


class OneShotSaver(Node):
    def __init__(self):
        super().__init__("jpeg_saver")

        # Subscribe once; the first callback will save and shut down.
        self.create_subscription(
            CompressedImage,
            "/camera/camera/color/image_rect_raw/compressed",
            self.save_and_quit,
            1,   # queue depth 1
        )

    # ───────────────────── callback ──────────────────────
    def save_and_quit(self, msg: CompressedImage):
        # build ~/Bachelor Thesis/realsense_pictures/
        folder = os.path.join(
            os.path.expanduser("~"),
            "Bachelor Thesis",
            "realsense_pictures",
        )
        os.makedirs(folder, exist_ok=True)

        # timestamped filename
        ts = self.get_clock().now().nanoseconds
        path = os.path.join(folder, f"color_{ts}.jpg")

        # write raw JPEG bytes
        with open(path, "wb") as f:
            f.write(msg.data)

        self.get_logger().info(f"Saved JPEG to {path}")
        rclpy.shutdown()          # stops spin(), process exits


def main(args=None):
    rclpy.init(args=args)
    node = OneShotSaver()
    rclpy.spin(node)
    # spin() returns after rclpy.shutdown() was called in save_and_quit


if __name__ == "__main__":
    main()