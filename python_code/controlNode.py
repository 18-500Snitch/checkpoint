# DONE: stub
# DONE: implement
# TODO: test

import constants
import math
import os
import sys

# FIFO
PIPE_PATH = "/tmp/rplidar.fifo"
MAX_BUF = 4096

HOVER_CONSTANT = 100 # the value at which the quad is barely hovering
DROP_CONSTANT = 10 # HOVER_CONSTANT-DROP_CONSTANT = slowly dropping
HOVER_HEIGHT = 100
BASE_SPEED = 50 # ele/til = BASE_SPEED/min_distance
SAFE_BUF = 0.7 # The Distance that the quadcopter will start moving away from things 
META = 3 # number of rplidar data points that are not actual data
# finished implementation
# not tested
class ControlNode:
    def __init__(self, topics):
        self.topics = topics
	# positive roll is right
	# positive pitch is forwards
	# positive thrust is up
        (self.roll, self.pitch, self.thrust) = (0, 0, 0)
        # FIFO
        # only want to create pipe once, should not assume which node creates first
        if not os.path.exists(PIPE_PATH):
            os.mkfifo(PIPE_PATH)

    def loop(self):
        (self.roll,self.pitch,self.thrust) = (0,0,0)
        command = self.topics[constants.BEHAVIOR_TOPIC]
        arduRange = (self.topics[constants.RANGEFINDER_TOPIC][0] + self.topics[constants.RANGEFINDER_TOPIC][1])/2

        if command == constants.BEHAVIOR_OFF:
            self.topics[constants.QUAD_TOPIC] = constants.RPLIDAR_DISARM
        elif command == constants.BEHAVIOR_HOVER:
            self.respondRangefinder(arduRange,command)
            self.respondRPLidar()
            self.topics[constants.QUAD_TOPIC] = self.filter()
        elif command == constants.BEHAVIOR_RESTING:
            self.respondRangefinder(arduRange,command)
            self.topics[constants.QUAD_TOPIC] = self.filter()
        elif command == constants.BEHAVIOR_ARM:
            self.topics[constants.QUAD_TOPIC] = constants.RPLIDAR_ARM
        elif command == constants.BEHAVIOR_DISARM:
            self.topics[constants.QUAD_TOPIC] = constants.RPLIDAR_DISARM
        elif command == constants.BEHAVIOR_TEST_RANGEFINDER:
            # hovers at HOVER_HEIGHT without response to rplidar
            # used for testing the rangefinder control loop
            self.respondRangefinder(arduRange,command)
            self.topics[constants.QUAD_TOPIC] = self.filter()
        elif command == constants.BEHAVIOR_TEST_RPLIDAR:
            # turn on throttle, but not enough to achieve flight, causing the quadcopter to act as a hovercraft
            # used for testing the rplidar without achieving flight
            self.thrust = HOVER_CONSTANT-DROP_CONSTANT
            self.respondRPLidar()
            self.topics[constants.QUAD_TOPIC] = self.filter()
        elif command == constants.BEHAVIOR_RANDOM:
            assert False # not yet implemented
        elif command == constants.BEHAVIOR_NULL:
            assert False # should never happen
        else:
            assert False

    def respondRangefinder(self,arduRange,behavior):
        thrust = 0
        if behavior == constants.BEHAVIOR_HOVER:
            thrust = HOVER_HEIGHT - arduRange
            thrust = thrust + HOVER_CONSTANT
        elif behavior == constants.BEHAVIOR_RESTING:
            if (arduRange < 10):
                thrust = 0
            elif (arduRange > 10):
                thrust = HOVER_CONSTANT-DROP_CONSTANT
        else:
            assert False
        self.thrust = thrust
		
    def respondRPLidar(self):
        # read data from rplidar_ros through fifo
        fifo = os.open(PIPE_PATH, os.O_RDONLY)
        rplidar_str = os.read(fifo, MAX_BUF)
        os.close(fifo)
        # parse string into data
        rplidar_data = [float(data) for data in rplidar_str.split()]
        (angle_min, angle_max, angle_inc) = rplidar_data[0:META]
        rplidar_data = rplidar_data[META:]
        # find nearest distance and angle
        near_only = [(theta, d) for (d, theta) in 
            enumerate(rplidar_data) if(d > 0)]
        (min_dist, angle) = min(near_only) if(near_only != []) else (None, None)
        if(angle):
            angle = angle_min + (angle * angle_inc) # actual angle
            # update pitch and roll
            (self.pitch, self.roll) = (int(-BASE_SPEED * math.cos(angle)),
                int(-BASE_SPEED * math.sin(angle))) if(min_dist < SAFE_BUF) else (0, 0)

    def filter(self):
        roll = self.roll
        pitch = self.pitch
        thrust = self.thrust
        if(abs(roll) > abs(pitch) and abs(roll) > 100):
            scaleFactor = abs(roll) / 100
            roll = roll / scaleFactor
            pitch = pitch / scaleFactor
        elif(abs(roll) < abs(pitch) and abs(pitch) > 100):
            scaleFactor = abs(pitch) / 100
            roll = roll / scaleFactor
            pitch = pitch / scaleFactor
        
        if thrust > 200: thrust = 200

        return roll, pitch, thrust, 0
