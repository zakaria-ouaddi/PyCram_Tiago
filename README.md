# PyCram_Tiago
setting up PyCram and Tiago robot

## Prerequisites

For this tutorial, you need to have **ROS Noetic** installed. Please follow the official ROS installation guide:

- [ROS Noetic Installation](https://wiki.ros.org/ROS/Installation)

## Setting Up PyCRAM

After installing ROS, you will need to set up **PyCRAM**. Follow the instructions in the PyCRAM documentation:

- [PyCRAM Installation Guide](https://pycram.readthedocs.io/en/latest/installation.html)

## Clone Required Repositories

Once you have set up ROS and PyCRAM, you will need to clone two repositories. Follow these steps:

1. Open the terminal.
2. Navigate to your workspace directory and then go to the `src` folder.
3. Clone the following repository:

   ```bash
   git clone https://github.com/pal-robotics/tiago_dual_robot
   ```

After cloning the repositories, follow the official tutorial to set up TIAGo with ROS:
-[Setting Up TIAGo with ROS](https://wiki.ros.org/Robots/TIAGo/Tutorials/Installation/InstallUbuntuAndROS)

##Launching the Setup

**Once everything is set up, you can launch the necessary components**
1. Open a terminal and run:

  ```bash
    roslaunch pycram ik_and_description.launch
  ```

2. In another terminal, open PyCharm using this command:

  ```bash
    ~/pycharm/bin/pycharm.sh
  ```


