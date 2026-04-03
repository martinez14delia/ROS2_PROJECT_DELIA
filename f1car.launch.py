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
        'mode': 'mapping'
    }]
)
    
    # TF para el lidar 
    static_tf = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=['0', '0', '0', '0', '0', '0', 'vehicle_red/chassis', 'vehicle_red/lidar_link/gpu_lidar']
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

    return LaunchDescription([
        gazebo,
        bridge,
        static_tf,
        slam_node,
    ])
