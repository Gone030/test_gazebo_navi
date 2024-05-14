import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    xacro_file = os.path.join(get_package_share_directory('test_gazebo'), 'urdf/', 'base.urdf.xacro')

    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    return LaunchDescription([
        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='true',
            description='use sim time'
        ),


        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=["-topic", "robot_description", "-entity", "test1"] #, "-x", "-2.5", "-y", "1.0", "-z", "0.2"]
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {"robot_description": robot_desc}
            ]
        )
    ])