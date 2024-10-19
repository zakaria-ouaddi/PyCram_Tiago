# Getting Started with TIAGo Robot and PyCRAM

## Overview

This guide will help you set up the necessary tools and environment to work with the **TIAGo robot** using **PyCRAM**. You'll learn how to install ROS Noetic, set up PyCRAM, and configure your workspace to get started with programming and controlling the TIAGo robot.

## Prerequisites

Before diving into the setup, there are a few essential tools and components you need to install.

### Step 1: Install ROS Noetic

**ROS (Robot Operating System)** is a flexible framework for writing robot software. It provides libraries and tools to help software developers create robot applications. 

For this tutorial, you will need **ROS Noetic**, which is the version compatible with **Ubuntu 20.04 (Focal)**. 

#### Installing Ubuntu

First, make sure your system is running Ubuntu 20.04. You can:
- **Download Ubuntu**: [Ubuntu 20.04 Desktop Download](https://ubuntu.com/download/desktop)
- **Run Ubuntu in a virtual environment**: Use a virtual machine or **Distrobox** for isolated environments. [Distrobox](https://distrobox.it/) is a tool that allows you to run Linux distributions inside a container.

#### Installing ROS Noetic

To install ROS Noetic, follow the official installation guide:

- [ROS Noetic Installation Guide](https://wiki.ros.org/noetic/Installation/Ubuntu)

### Step 2: Set Up PyCRAM and Install PyCharm Professional

After ROS Noetic is installed, the next step is to set up **PyCRAM**, a cognitive robotic programming framework that simplifies writing robot control programs.

1. Follow the setup instructions provided in the PyCRAM documentation:
   - [PyCRAM Installation Guide](https://pycram.readthedocs.io/en/latest/installation.html)

2. Install **PyCharm Professional**, an integrated development environment (IDE) for Python, which will make it easier to manage your code and projects. You can download it from the [JetBrains website](https://www.jetbrains.com/pycharm/download/).

### Step 3: Clone the Required Repositories

With ROS Noetic and PyCRAM set up, you need to clone two repositories into your workspace.

1. Open your terminal and navigate to the `src` folder of your workspace. You can do this with the following command:

   ```bash
   cd ~/workspace/ros/src
   ```
2. In this src folder, you should already have folders like iai_maps, iai_robots, kdl_ik_services, and pycram. Now, you need to add two more repositories:
 - **TIAGo Dual Robot**: This repository contains the essential files for controlling the TIAGo robot.
   ```bash
   git clone https://github.com/pal-robotics/tiago_dual_robot
   ```
- **TIAGo Public Files**: Follow the steps provided in the [TIAGo ROS Setup Guide](https://wiki.ros.org/Robots/TIAGo/Tutorials/Installation/InstallUbuntuAndROS) to set this up.

## Building Your Workspace
  - After cloning the repositories, it's essential to build your workspace. Always use ***catkin_make*** for this, as it is the build tool used during the PyCRAM setup.

## Launching and Running Your First Python Script with TIAGo and PyCRAM
 
 You are now ready to launch your first script with the TIAGo robot using PyCRAM.
 
 **Step 1: Start PyCharm**
 Open PyCharm from your terminal:
```bash
~/pycharm-(version)/bin/pycharm.sh
```
***Note***: Replace pycharm-(version) with the specific version folder name, such as pycharm-2024.2.3.

**Step 2: Launch the ROS Server**
Step 2: Launch the ROS Server
```bash
roslaunch pycram ik_and_description.launch
```

**Step 3: Open the Project in PyCharm**
1. In PyCharm, click on File (top-left corner) and choose Open.
2. Navigate to your src folder within your workspace and open the pycram folder.
3. Add the following repository to the project:
   -TIAGo Robot Work: [PyCRAM_Tiago](https://github.com/zakaria-ouaddi/PyCram_Tiago)
   -You can add it either by cloning it directly in PyCharm or by downloading and importing it.

**Step 4: Run the Python Files**
Now, you can start running the Python scripts within PyCharm to interact with the TIAGo robot.

**Additional Tips**
- Always ensure that your ROS environment is correctly sourced before running any ROS-related commands:
```bash
source ~/workspace/ros/devel/setup.bash
```
- Use catkin_make for any changes in the workspace to make sure everything compiles correctly.

