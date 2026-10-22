# 🤖 MY_robot — ROS 2 + Ignition Gazebo Simulation

> A fully simulated robot built with ROS 2 (Humble) and Ignition Gazebo (Fortress), featuring a SolidWorks-designed model exported to URDF/SDF, LiDAR & ultrasonic sensors, odometry, SLAM-based mapping, and keyboard teleoperation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Build](#️-build)
- [Usage](#-usage)
- [Notes & Troubleshooting](#-notes--troubleshooting)
- [Features](#-features)

---

## Overview

MY_robot is a full-stack robotics simulation project that covers the complete pipeline from mechanical CAD design to autonomous environment mapping, built entirely on ROS 2 (Humble) and Ignition Gazebo (Fortress). The robot was mechanically designed in SolidWorks as a wheeled platform with independent suspension geometry across all four wheels. The CAD assembly was exported using the SolidWorks URDF Exporter, producing a URDF file with accurate joint axes, link inertial properties, and STL mesh references, which was then adapted into an SDF format compatible with Ignition Gazebo.

The robot is simulated inside a custom Gazebo world built with a terrain heightmap and a textured ground plane, creating a realistic uneven environment for testing sensor behavior and navigation. Simulation is managed through a modular set of ROS 2 launch files that separately handle robot spawning, topic bridging, and RViz2 visualization, making it easy to run or debug individual components independently.

For sensing, the robot is equipped with a LiDAR that publishes 2D laser scan data on the /scan topic, serving as the primary input for SLAM-based mapping and obstacle detection, alongside ultrasonic sensors that provide short-range proximity measurements to cover blind spots within LiDAR's minimum range. The robot also publishes an odom reference frame that tracks its estimated position and orientation over time using wheel encoder data, forming the base of the ROS 2 TF tree and anchoring the SLAM map to the robot's trajectory.

Using SLAM Toolbox in online_async mode, the robot builds a real-time 2D occupancy grid map as it moves through the environment by fusing LiDAR scans with odometry data. The resulting map can be saved and reused for future autonomous navigation tasks. The robot is driven manually through a keyboard teleoperation node that publishes Twist velocity commands over ROS 2 topics, which are translated to Ignition Gazebo through the ROS–Ignition bridge — allowing the operator to explore the world and accumulate the sensor data needed for mapping.

---

## 📁 Project Structure

```
MY_robot/
├── solidworks_files/                   # Original SolidWorks CAD model (.SLDPRT / .SLDASM)
│                                       # Used to generate the robot URDF via sw_urdf_exporter
├── .gitignore
├── README.md
└── src/my_robot/
    ├── config/                         # ROS 2 parameter & SLAM Toolbox configs
    ├── launch/
    │   ├── main_gazebo.launch.py       # Master launch (sim + bridge + rviz)
    │   ├── robot_gazebo.launch.py      # Spawn robot in Gazebo
    │   ├── bridge.launch.py            # ROS–Ignition topic bridge
    │   └── rviz.launch.py              # RViz2 visualization
    ├── meshes/                         # STL mesh files exported from SolidWorks
    │   ├── base_link.STL
    │   ├── f_l_s.STL                   # Front-left suspension
    │   ├── f_l_w.STL                   # Front-left wheel
    │   ├── f_r_s.STL                   # Front-right suspension
    │   ├── f_r_w.STL                   # Front-right wheel
    │   ├── r_l_s.STL                   # Rear-left suspension
    │   ├── r_l_w.STL                   # Rear-left wheel
    │   ├── r_r_s.STL                   # Rear-right suspension
    │   └── r_r_w.STL                   # Rear-right wheel
    ├── scripts/
    │   └── teleop_controller.py        # Keyboard teleoperation node with built-in PID control for smooth velocity output 
    ├── urdf/
    │   ├── my_robot.urdf               # Robot URDF (joints, links, sensors)
    │   ├── my_robot.sdf                # SDF version for Ignition Gazebo
    │   └── my_robot.csv                # Joint/link metadata (sw_urdf_exporter output)
    ├── world/
    │   ├── world.sdf                   # Gazebo simulation world
    │   ├── dirt.png                    # Ground texture
    │   └── earthquake_heightmap.png    # Terrain heightmap
    ├── CMakeLists.txt
    └── package.xml
```

---

## 📦 Requirements

| Dependency | Version | Install |
|---|---|---|
| ROS 2 | Humble | `sudo apt install ros-humble-desktop` |
| Ignition Gazebo | Fortress | `sudo apt install ignition-fortress` |
| ROS–Ignition Bridge | — | `sudo apt install ros-humble-ros-ign` |
| SLAM Toolbox | — | `sudo apt install ros-humble-slam-toolbox` |
| colcon | latest | `sudo apt install python3-colcon-common-extensions` |

> **OS:** Ubuntu 22.04 is recommended for ROS 2 Humble + Ignition Fortress compatibility.

---

## 🔧 Installation

### 1. Install ROS 2 Humble

```bash
sudo apt update
sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash
```

To avoid sourcing manually every session, add it to your shell profile:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### 2. Install Ignition Gazebo (Fortress)

```bash
sudo apt install ignition-fortress
```

### 3. Install the ROS–Ignition Bridge

```bash
sudo apt install ros-humble-ros-ign
```

### 4. Install SLAM Toolbox

```bash
sudo apt install ros-humble-slam-toolbox
```

### 5. Install colcon Build Tool

```bash
sudo apt install python3-colcon-common-extensions
```

---

## 🛠️ Build

Navigate to the workspace root and build with colcon:

```bash
cd ~/ROS_PROJECT/MY_robot
colcon build
```

Then source the workspace overlay:

```bash
source install/setup.bash
```

> **Tip:** Add `source ~/ROS_PROJECT/MY_robot/install/setup.bash` to your `~/.bashrc` to auto-source on every terminal session.

---

## 🚀 Usage

Run each command in a **separate terminal**, with the workspace sourced in each one.

### Step 1 — Launch the Simulation

```bash
ros2 launch my_robot main_gazebo.launch.py
```

### Step 2 — Start the ROS–Ignition Bridge

```bash
ros2 launch my_robot bridge.launch.py
```

### Step 3 — Launch SLAM Toolbox (Mapping)

```bash
ros2 launch slam_toolbox online_async_launch.py
```

> This begins building a 2D occupancy map using LiDAR data. Open RViz2 and add the `/map` topic to visualize it in real time.

### Step 4 — Run the Teleoperation Controller

```bash
ros2 run my_robot teleop_controller.py
```

Use the keyboard to drive the robot and explore the environment while SLAM builds the map.

### Step 5 — Visualize the SLAM Map in RViz2
Once the simulation, bridge, and SLAM Toolbox are all running, open RViz2 to monitor the mapping process in real time:

- Add a LaserScan display and set its topic to /scan to visualize LiDAR data
- Add a Map display and set its topic to /map to see the occupancy grid being built
- Enable TF to visualize the active transform frames
- Set the Fixed Frame to odom


> Note: Gazebo, the ROS–Ignition bridge, and SLAM Toolbox must all be running before launching RViz2, otherwise the /map and /scan topics will not be available.

### Step 6 — Visualize the Robot Model in RViz2
To inspect the robot's physical structure and its TF frame tree, launch the dedicated RViz2 launch file:
```bash
ros2 launch my_robot rviz.launch.py
```

Inside RViz2:

- Add a RobotModel display and set its description topic to /robot_description to render the full robot geometry
- Enable TF to visualize all active coordinate frames
- Set the Fixed Frame to base_footprint


> Note: The robot model in RViz2 is loaded from the URDF file, not the SDF. This is because the /robot_description topic is populated by the robot_state_publisher node, which only accepts URDF — SDF files are not supported for this purpose.
---

## 🔍 Notes & Troubleshooting

### Gazebo fails to launch (WSL / headless / virtual machine)

If you're running inside WSL or a system without a proper GPU, Gazebo may fail due to graphics rendering issues. Use software rendering as a workaround:

```bash
LIBGL_ALWAYS_SOFTWARE=1 QT_QPA_PLATFORM=xcb ros2 launch my_robot main_gazebo.launch.py
```

### SLAM map not building

- Ensure the ROS–Ignition bridge is running and LiDAR scan data is being published on `/scan`
- Verify the `odom` frame is being published: `ros2 topic echo /odom`
- Check that the SLAM Toolbox config in `config/` has the correct topic and frame names

### Always source before running

Every new terminal session needs the workspace sourced:

```bash
source /opt/ros/humble/setup.bash
source ~/ROS_PROJECT/MY_robot/install/setup.bash
```

### Rebuild after making changes

If you modify any source files, rebuild before running:

```bash
colcon build --symlink-install
source install/setup.bash
```

---

## ✨ Features

- 🌍 **Ignition Gazebo simulation** — physics-based robot environment with custom terrain world
- 🦾 **SolidWorks CAD model** — robot designed in SolidWorks and exported to URDF via `sw_urdf_exporter`
- 📐 **Custom URDF/SDF** — simulation-ready model with joints, links, meshes, and sensor definitions
- 📡 **LiDAR sensor** — 2D laser scan published on `/scan` for SLAM and obstacle detection
- 🔊 **Ultrasonic sensors** — proximity sensing for short-range obstacle awareness
- 🧭 **Odometry frame** (`odom`) — reference frame for tracking robot position over time
- 🗺️ **SLAM Toolbox mapping** — real-time 2D occupancy map generation while driving
- 🕹️ **Teleoperation** — keyboard-based robot driving over ROS 2 topics
- 🔗 **ROS–Ignition bridge** — bidirectional topic translation between ROS 2 and Ignition
- 📊 **RViz2 visualization** — real-time display of robot state, sensor data, and SLAM map

---
