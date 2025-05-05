"""Send six CartesianSpace goals sequentially.

Runs as a ROS 2 node (`send_goals`).  The script sends each pose to the
`/cartesian_space` service, waits until planning+execution succeeds, pauses
for two seconds, and then proceeds to the next pose.

Edit the `poses` list in `main()` if you want to change or re‑order the goals.
"""

import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from moveit_msg.srv import CartesianSpace


def make_pose(x: float, y: float, z: float,
              ox: float, oy: float, oz: float, ow: float) -> Pose:
    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    pose.position.z = z
    pose.orientation.x = ox
    pose.orientation.y = oy
    pose.orientation.z = oz
    pose.orientation.w = ow
    return pose


class SendGoals(Node):
    """ROS 2 client node that sends CartesianSpace goals in sequence."""

    def __init__(self) -> None:
        super().__init__('send_goals')
        self.cli = self.create_client(CartesianSpace, '/cartesian_space')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /cartesian_space service …')
        self.req = CartesianSpace.Request()

    def send_pose(self, pose: Pose):
        self.req.target_pose = pose
        return self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    node = SendGoals()

    # ──► 6 target poses. Edit these values to suit your application.
    poses = [
        make_pose(0.270, -0.258, 0.400, 0.885, -0.466, 0.0052, -0.0038),
        make_pose(0.300, -0.200, 0.350, 0.885, -0.466, 0.0052, -0.0038),
        make_pose(0.200, -0.150, 0.450, 0.885, -0.466, 0.0052, -0.0038),
        make_pose(0.250, -0.300, 0.420, 0.885, -0.466, 0.0052, -0.0038),
        make_pose(0.270, -0.258, 0.500, 0.885, -0.466, 0.0052, -0.0038),
        make_pose(0.240, -0.230, 0.380, 0.885, -0.466, 0.0052, -0.0038),
    ]

    for idx, pose in enumerate(poses, 1):
        node.get_logger().info(f'Sending goal {idx}/6 …')
        future = node.send_pose(pose)
        rclpy.spin_until_future_complete(node, future)

        result = future.result()
        if result is not None and result.success:
            node.get_logger().info(f'Goal {idx} reached. ✅')
        else:
            err = '' if result is None else result.error_message
            node.get_logger().error(f'Goal {idx} failed: {err}')
            break  # stop if any goal fails

        time.sleep(2.0)  # wait 2 s before the next goal

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
