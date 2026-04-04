import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('f1car_pkg')
    sdf_file = os.path.join(pkg_dir, 'worlds', 'car_diff8.sdf')
    map_file = os.path.join(pkg_dir, 'maps', 'f1_map_v3.yaml')
    nav2_params = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')
    nav2_bringup = get_package_share_directory('nav2_bringup')

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', sdf_file],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/model/vehicle_red/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/model/vehicle_red/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
        ],
        remappings=[
            ('/model/vehicle_red/odometry', '/odom'),
            ('/model/vehicle_red/tf', '/tf'),
        ],
        output='screen'
    )

    tf_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_lidar',
        arguments=[
            '--x', '0.25', '--y', '0', '--z', '0.25',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'vehicle_red/chassis',
            '--child-frame-id', 'vehicle_red/lidar_link/gpu_lidar'
        ],
        output='screen'
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': 'True',
            'params_file': nav2_params,
        }.items()
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(nav2_bringup, 'rviz', 'nav2_default_view.rviz')],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        bridge,
        tf_lidar,
        nav2,
        rviz,
    ])
