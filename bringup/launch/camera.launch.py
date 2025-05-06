from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():

    # 1. Node that moves the robot to the photo pose and then quits
    home_camera_node = Node(
        package='goal_client',
        executable='home_camera',   # ← your new console‑script
        name='home_camera',         # node name inside the script
        output='screen',
    )

    # 2. Node that saves the RGB‑D image
    save_image_node = Node(
        package='jpeg_saver',
        executable='save_image',
        name='save_image',
        output='screen',
    )

    # Start save_image only after home_camera has finished
    start_image_after_goal = RegisterEventHandler(
        OnProcessExit(
            target_action=home_camera_node,   # watch home_camera
            on_exit=[save_image_node],        # then launch save_image
        )
    )

    # home_camera starts immediately; save_image is triggered by the handler.
    return LaunchDescription([
        home_camera_node,
        start_image_after_goal,
    ])