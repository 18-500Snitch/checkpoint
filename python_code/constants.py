# constants and utilities and structs


import time

BEHAVIOR_TOPIC = "Behavior"  # string enums
RPLIDAR_TOPIC = "RPLidar"  # [rplidarDatapoint]
QUAD_TOPIC = "Quad"  # (ail, ele, rud)
THRUST_TOPIC = "Thrust"
RANGEFINDER_TOPIC = "Rangefinder"  # (left, right)
UDP_TOPIC = "Udp"

#
#BEHAVIOR_NULL = "NULL" # invalid response
#BEHAVIOR_HOVER = "HOVER" # hover while avoiding objects
#BEHAVIOR_RANDOM = "RANDOM" # move randomly if no collision imminent
#BEHAVIOR_RESTING = "RESTING" # landing
#BEHAVIOR_OFF = "OFF" # force off
#BEHAVIOR_ARM = "ARM"
#BEHAVIOR_DISARM = "DISARM"
#BEHAVIOR_TEST_RANGEFINDER = "RANGEFINDER"
#BEHAVIOR_TEST_RPLIDAR = "RPLIDAR"

# UDP messages
CMD_ARM = "A\n"
CMD_DISARM = "D\n"
CMD_FLOAT = "0\n"
CMD_FWD = "UP\n"
CMD_BCK = "DN\n"
CMD_LFT = "LT\n"
CMD_RHT = "RT\n"
CMD_RISE = " \n"
CMD_DECEND = "b\n"
CMD_OFF = "o\n"

# Control Constants
DISARM = (1500,1500,1000)
ARM    = (1500,1500,2000)
FLOAT = (1500,1500,1500)
LEAN_FWD = (1500,1525,1500)
LEAN_BCK = (1500,1475,1500)
LEAN_LFT = (1475,1500,1500)
LEAN_RHT = (1520,1500,1500)
RISE = 5
DECEND = 5
OFF = (1500,1500,1500)

STDIN_INDEX = 0
STDOUT_INDEX = 1
STDERR_INDEX = 2

FREQUENCY = 1.0/20

def millis():
    return int(time.time()*1000)
