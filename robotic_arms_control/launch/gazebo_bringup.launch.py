import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkgPath = get_package_share_directory('robotic_arms_control')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    urdf_file = os.path.join(pkgPath, 'urdf', 'panda_arm.urdf')
    config_file = os.path.join(pkgPath, 'config', 'panda_jtc_controller.yaml')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Ensure parameter path in URDF points to the valid config file
    robot_desc = robot_desc.replace(
        '/home/luqman/udemy_ws/src/robotic_arms_control/config/panda_jtc_controller.yaml',
        config_file
    )

    # Mesh discovery for Gazebo Sim Harmonic
    franka_share = os.path.join(get_package_prefix('franka_description'), 'share')
    set_gz_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        franka_share
    )

    # 1. Gazebo Harmonic Simulation Engine
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 2. Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }]
    )

    # 3. Spawn Panda Arm entity in Gazebo Sim
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        name='robot_spawner',
        output='screen',
        arguments=[
            '-name', 'panda',
            '-topic', '/robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0'
        ]
    )

    # 4. ROS-Gz Bridge for clock
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        output='screen',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        bridge
    ])