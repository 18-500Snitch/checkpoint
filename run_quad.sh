#!/bin/bash

# just quad, no SLAM, run in new tmux window
tmux split -h

tmux selectp -t 0 # left RPLIDAR
cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash
source /opt/ros/kinetic/setup.bash
roslaunch rplidar_ros rplidar.launch

tmux selectp -t 1 # right Python
cd ~/checkpoint/python_code
python main.py
