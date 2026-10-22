from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction
from launch_ros.actions import Node
import os
from launch_ros.actions import Node


def generate_launch_description():

    #Set resource path
    set_env = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '') +
              ':/home/sidharth/MY_robot/install/my_robot/share'
    )

    #Spawn robot
    spawn_robot = TimerAction(
        period=2.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ign', 'service',
                    '-s', '/world/earthquake_disaster/create',
                    '--reqtype', 'ignition.msgs.EntityFactory',
                    '--reptype', 'ignition.msgs.Boolean',
                    '--timeout', '5000',
                    '--req',
                    'sdf_filename: "/home/sidharth/MY_robot/install/my_robot/share/my_robot/urdf/my_robot.sdf", '
                    'name: "my_robot", pose: {position: {x: 0, y: 0, z: 0.5}}'
                ],
                output='screen'
            )
        ]
    )

    #Bridge
    bridge = Node(
    package='ros_ign_bridge',
    executable='parameter_bridge',
    arguments=[
        '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
        '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
        '/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan',
        '/tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V',
        '/ultrasonic/front@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan',
    ],
    output='screen'
)
    
    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0', '0', '0.16',
            '0', '0', '0',
            'base_footprint',
            'lidar_link'
        ]
    )

    ultra_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.22', '0', '0.08',
            '0', '0', '0',
            'base_footprint',
            'ultrasonic_front'
        ]
    )

    return LaunchDescription([
        set_env,
        spawn_robot,
        bridge,
        lidar_tf,
        ultra_tf
    ])