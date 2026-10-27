import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    description_share = get_package_share_directory("scoutnav_description")
    bringup_share = get_package_share_directory("scoutnav_bringup")
    world = os.path.join(bringup_share, "worlds", "simple_world.sdf")
    xacro_file = os.path.join(description_share, "urdf", "scoutnav.urdf.xacro")
    import xacro
    robot_description = xacro.process_file(xacro_file).toxml()
    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world}"}.items(),
    )
    state_publisher = Node(
        package="robot_state_publisher", executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
        output="screen",
    )
    spawn = Node(
        package="ros_gz_sim", executable="create",
        arguments=["-name", "scoutnav", "-topic", "robot_description", "-x", "0", "-y", "0", "-z", "0.12"],
        output="screen",
    )
    controller = Node(
        package="scoutnav_controller", executable="reactive_controller",
        parameters=[{"use_sim_time": True}], output="screen",
    )
    return LaunchDescription([gz, state_publisher, spawn, bridge, controller])
