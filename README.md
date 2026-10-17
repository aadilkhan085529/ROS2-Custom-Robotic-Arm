# ROS 2 Ultimate Guide for Custom Robotic Arms and Panda 7 DOF

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-this-repository">About This Repository</a></li>
    <li><a href="#workspace-setup--build">Workspace Setup & Build</a></li>
    <li><a href="#commands-reference">Commands Reference</a>
      <ul>
        <li><a href="#1-rviz2-visualization">1. RViz2 Visualization</a></li>
        <li><a href="#2-gazebo-simulation--ros2_control">2. Gazebo Simulation & ros2_control</a></li>
        <li><a href="#3-interactive-slider-control-gui">3. Interactive Slider Control GUI</a></li>
        <li><a href="#4-trajectory-execution">4. Trajectory Execution</a></li>
        <li><a href="#5-kinematics-solvers-fk--ik">5. Kinematics Solvers (FK & IK)</a></li>
        <li><a href="#6-tf-transform-broadcasting">6. TF Transform Broadcasting</a></li>
      </ul>
    </li>
    <li><a href="#course-workflow">Course Workflow</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#notes--resources">Notes & Resources</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

---

## About This Repository

This repository contains the complete code for the project-based course **ROS 2 Ultimate Guide for Custom Robotic Arms and Panda 7 DOF**. It covers robot modeling, DH parameters, forward and inverse kinematics using Peter Corke's Robotics Toolbox for Python, `ros2_control` architectures, Gazebo physics simulation, and trajectory execution for both a custom educational arm (**BAZU**) and an industrial 7-DOF arm (**Franka Emika Panda**).

![Course Thumbnail](https://github.com/noshluk2/ROS2-Ultimate-guide-for-Custom-Robotic-Arms-and-Panda-7-DOF/blob/master/Images/thumbnail.png)

* **[[Get Course Access]](https://robotisim.com/project-based-course/)**

---

## Workspace Setup & Build

### 1. Build the Workspace
From the workspace root (`~/ros2_ws`):
```bash
cd ~/ros2_ws
colcon build --symlink-install
```

To build only the robotic arm packages:
```bash
colcon build --symlink-install --packages-select franka_description robotic_arms_control
```

### 2. Source the Workspace
Always source the workspace in every new terminal before running commands:
```bash
source ~/ros2_ws/install/setup.bash
```

---

## Commands Reference

### 1. RViz2 Visualization

#### Franka Emika Panda Arm
Visualizes the 7-DOF Panda arm with high-resolution visual and collision meshes, along with the interactive Joint State Publisher GUI slider window:
```bash
ros2 launch franka_description visualize_franka.launch.py
```
> **Optional**: To load without the Franka hand/gripper:
> ```bash
> ros2 launch franka_description visualize_franka.launch.py load_gripper:=false
> ```

#### Custom Arm (BAZU) / Panda Model Bringup
Visualizes the arm model in RViz2:
```bash
ros2 launch robotic_arms_control rviz_bringup.launch.py
```

---

### 2. Gazebo Simulation & ros2_control

#### Launch Gazebo Simulation, Spawn Arm & Start Controllers
Brings up the Gazebo simulation engine, loads the robot description, spawns the arm, and activates the controller spawners (`joint_state_broadcaster` and `joint_trajectory_controller`):
```bash
ros2 launch robotic_arms_control controller_spawner.launch.py
```

#### Launch Gazebo Bringup Only
Spawns the Panda arm in an empty Gazebo world with the ROS-Gazebo clock bridge:
```bash
ros2 launch robotic_arms_control gazebo_bringup.launch.py
```

---

### 3. Interactive Slider Control GUI

Control the simulated arm in real time using interactive graphical sliders:

```bash
ros2 run rqt_joint_trajectory_controller rqt_joint_trajectory_controller
```

**Steps to operate:**
1. In the top dropdown, select `/controller_manager`.
2. In the controller dropdown, select `joint_trajectory_controller`.
3. Click the circular power toggle on the left to turn it **green (enabled)**.
4. Drag the sliders for `panda_joint1` through `panda_finger_joint1` to move the arm in Gazebo.

---

### 4. Trajectory Execution

With the Gazebo simulation and controller spawner running in another terminal:

#### A. Single Goal Trajectory Test
Publishes a predefined trajectory goal to `/joint_trajectory_controller/joint_trajectory`:
```bash
ros2 run robotic_arms_control jtc_controller_test
```

#### B. Multi-Goal Waypoint Trajectory Test
Executes sequential trajectory waypoints, moving the arm through a complex sequence of poses:
```bash
ros2 run robotic_arms_control jtc_multi_goals
```

---

### 5. Kinematics Solvers (FK & IK)

#### A. Target Coordinate Inverse Kinematics Controller
Computes Levenberg-Marquardt inverse kinematics for given Cartesian coordinates $(X, Y, Z)$ and commands the arm:
```bash
ros2 run robotic_arms_control kinematic_solver 0.0 0.7 0.5
```
*(Replace `0.0 0.7 0.5` with your desired target $(X, Y, Z)$ in meters).*

#### B. Standalone Forward & Inverse Kinematics Script
Computes FK for joint angles and IK for a 3D pose using Peter Corke's Robotics Toolbox:
```bash
python3 src/robotic_arms_control/robotic_arms_control/rtb_ikine_fkine.py
```

#### C. Interactive Kinematics Jupyter Notebook
Interactive tutorial stepping through transformation matrices, DH tables, and analytical/numerical IK:
```bash
jupyter notebook "Robotics_kinematics_solver.ipynb"
```

---

### 6. TF Transform Broadcasting

Broadcasts static coordinate transforms between `Base`, `Link_0`, and `Link_1`:
```bash
ros2 run robotic_arms_control transforms_pub
```

Inspect the active transform tree in another terminal:
```bash
ros2 run tf2_tools view_frames
```

---

## Course Workflow

1. **Custom Manipulator (BAZU)**: Created from scratch using URDF primitives (links and revolute joints), calculating moments of inertia, and configuring `ros2_control` hardware interfaces.
2. **Controller Integration**: Implementation of `ForwardCommandController`, `JointStateBroadcaster`, and `JointTrajectoryController`.
3. **Kinematics with Robotics Toolbox**: Derivation of DH parameter tables and solving Forward Kinematics (FK) and Inverse Kinematics (IK) using `roboticstoolbox-python` and `spatialmath`.
4. **Commercial Arm (Franka Emika Panda 7-DOF)**: Mesh integration, joint trajectory control, and Cartesian trajectory execution.
5. **Multi-Goal Path Execution**: Automated waypoint generation and path execution in simulation.

---

## Features

* **Building Custom Robotic Arm**  
  ![Custom Arm](https://github.com/noshluk2/ROS2-Ultimate-guide-for-Custom-Robotic-Arms-and-Panda-7-DOF/blob/master/Images/1_custom_arm.gif)

* **Controllers Test**  
  ![Controllers Test](https://github.com/noshluk2/ROS2-Ultimate-guide-for-Custom-Robotic-Arms-and-Panda-7-DOF/blob/master/Images/2_bazu_controller.gif)

* **Joint Trajectories**  
  ![Joint Trajectories](https://github.com/noshluk2/ROS2-Ultimate-guide-for-Custom-Robotic-Arms-and-Panda-7-DOF/blob/master/Images/3_panda_jtc.gif)

* **Multi Goal Trajectories**  
  ![Multi Goal Trajectories](https://github.com/noshluk2/ROS2-Ultimate-guide-for-Custom-Robotic-Arms-and-Panda-7-DOF/blob/master/Images/4_panda_multi_goal.gif)

---

## Notes & Resources

* Complete lecture notes with mathematical derivations, DH parameter diagrams, and controller configuration guides are included in [`Notes/Complete_notes.pdf`](Notes/Complete_notes.pdf).

---

## License

Distributed under the GNU-GPL License. See `LICENSE` for more information.
