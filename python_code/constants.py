# constants and utilities and structs


import time

BEHAVIOR_TOPIC = "Behavior"  # string enums
RPLIDAR_TOPIC = "RPLidar"  # [rplidarDatapoint]
QUAD_TOPIC = "Quad"  # (ail, ele, thr, rud)
RANGEFINDER_TOPIC = "Rangefinder"  # (left, right)

BEHAVIOR_NULL = "NULL" # invalid response
BEHAVIOR_HOVER = "HOVER" # hover while avoiding objects
BEHAVIOR_RANDOM = "RANDOM" # move randomly if no collision imminent
BEHAVIOR_RESTING = "RESTING" # landing
BEHAVIOR_OFF = "OFF" # force off
BEHAVIOR_ARM = "ARM"
BEHAVIOR_DISARM = "DISARM"
BEHAVIOR_TEST_RANGEFINDER = "RANGEFINDER"
BEHAVIOR_TEST_RPLIDAR = "RPLIDAR"

RPLIDAR_DISARM = (0,0,-5,98)
RPLIDAR_ARM    = (0,0,-5,-98)

STDIN_INDEX = 0
STDOUT_INDEX = 1
STDERR_INDEX = 2

FREQUENCY = 1.0/20


class RPLidarDatapoint:
    def __init__(self, valid, angle, distance):
        self.valid = valid
        self.angle = angle
        self.distance = distance
    def __repr__(self):
        return "(V:"+str(self.valid)+" A:"+str(self.angle)+" D:"+str(self.distance) + ")"

def millis():
    return int(time.time()*1000)
