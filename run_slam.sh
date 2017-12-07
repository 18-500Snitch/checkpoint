#!/bin/bash

# should be run in new tmux window
# setup roscore and slam
cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash
source /opt/ros/kinetic/setup.bash
roscore
MASTER_URL = localhost # TODO 
export ROS_MASTER_URI=$MASTER_URL
roslaunch hector_slam_launch tutorial.launch &

# start quad
tmux splitw -h
tmux selectp -t 1 # right pane for quad
ssh Bench8-4B-Fly@localhost # TODO quad
tmux split -v

tmux selectp -t 1 # top pane for RPLIDAR
cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash
source /opt/ros/kinetic/setup.bash
export ROS_MASTER_URI=$MASTER_URL
roslaunch rplidar_ros rplidar.launch &

tmux selectp -t 2 # bottom pane for Python
cd ~/checkpoint/python_code
python main.py &
