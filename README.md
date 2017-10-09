# checkpoint

*Explanation of Python*
The implementation of the python files is essentially a verys simple version of ROS

*Utility*
constants.py     : constants and utility
rosLib.py        : ros library
udpReceiver.py   : utility for recieving messages over wifi

*ROS nodes*
arduinoNode.py   : responsible for communication to arduino relay
controlNode.py   : responsible for control and feedback and motion
executiveNode.py : responsible for overall action, and wifi relay
rplidarNode.py   : responsible for communication to rplidar c file

*ROS topics*
Quad Pwm         : (ail, ele, thr, rud)
Rangefinder      : (left, right)
Behavior         : int
RPLidar          : [(quality, angle, distance)]

*Other*
main.py          : putting it all together, run this file
rplidar_sdk/output/Linux/Release/ultra_simple : this file is activated by rplidarNode.py, but you can mess with it yourself
rplidar_sdk/app/ultra_simple/main.cpp         : source code of a highly modified version of the original ultra_simple app

Instructions:
$ cd $HOME/checkpoint/rplidar_sdk
$ make
$ python $HOME/checkpoint/python_code/main.py