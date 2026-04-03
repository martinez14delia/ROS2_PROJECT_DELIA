import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('f1car_pkg')
    sdf_file = os.path.join(pkg_dir, 'worlds', 'car_diff8.sdf')

    # Arrancar Gazebo con el circuito
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', sdf_file],
        output='screen'
    )
    
    # Bridge
    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
        '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
        '/model/vehicle_red/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
        '/model/vehicle_red/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V', # <--- Importante para SLAM
    ],
    remappings=[
        ('/model/vehicle_red/odometry', '/odom'),
        ('/model/vehicle_red/tf', '/tf'),
    ],
    output='screen'
)

    # TF lidar->chassis (posición del lidar en el SDF: x=0.25, z=0.10)
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
    
    # para usar el SLAM
    slam_node = Node(
    package='slam_toolbox',
    executable='async_slam_toolbox_node',
    name='slam_toolbox',
    output='screen',
    parameters=[{
        'use_sim_time': True,
        'odom_frame': 'vehicle_red/odom',
        'base_frame': 'vehicle_red/chassis',
        'scan_topic': '/scan',
        'mode': 'mapping',
        'max_laser_range':50.0,
        'resolution': 0.05,
        'minimum_travel_distance':0.1,
        'minimum_travel_heading':0.1,
    }]
)
    
    return LaunchDescription([
        gazebo,
        bridge,
        tf_lidar,
        slam_node,
    ])
