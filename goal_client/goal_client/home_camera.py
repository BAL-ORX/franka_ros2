"""
home_camera – send ONE Cartesian‑space goal, then quit.

Intended to run first in your bring‑up launch; when the node exits
`OnProcessExit` will trigger the image‑capture node.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from moveit_msg.srv import CartesianSpace


def make_pose(x, y, z, ox, oy, oz, ow):
    p = Pose()
    p.position.x, p.position.y, p.position.z = x, y, z
    p.orientation.x, p.orientation.y, p.orientation.z, p.orientation.w = ox, oy, oz, ow
    return p


class HomeCamera(Node):
    def __init__(self):
        super().__init__('home_camera')
        self.cli = self.create_client(CartesianSpace, '/cartesian_space')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /cartesian_space service …')
        self.req = CartesianSpace.Request()

    def send_goal(self, pose: Pose):
        self.req.target_pose = pose
        return self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    node = HomeCamera()

    # ✏️  Put your *single* photo‑taking pose here
    start_pose = make_pose(
        0.640,   # x [m]
        -0.003,  # y
        0.600,   # z
        0.916,   # qx
        -0.402,  # qy
        0.006,  # qz
        -0.014  # qw
    )

    node.get_logger().info('Sending home‑camera goal …')
    future = node.send_goal(start_pose)
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    if result and result.success:
        node.get_logger().info('Home‑camera position reached ✅')
    else:
        err = '' if result is None else result.error_message
        node.get_logger().error(f'Failed to reach home pose: {err}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()