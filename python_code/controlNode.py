# DONE: stub
# DONE: implement
# TODO: test

import constants
import math
import os
import sys

PIPE_PATH = "/tmp/rplidar.fifo"

HOVER_CONSTANT = 100 # the value at which the quad is barely hovering
DROP_CONSTANT = 10 # HOVER_CONSTANT-DROP_CONSTANT = slowly dropping
HOVER_HEIGHT = 100
BASE_SPEED = 50 # ele/til = BASE_SPEED/min_distance
MAX_DISTANCE = 600 # The Distance that the quadcopter will start moving away from things 
# finished implementation
# not tested
class ControlNode:
    def __init__(self, topics):
        self.topics = topics
	# positive roll is right
	# positive pitch is forwards
	# positive thrust is up
        (self.roll, self.pitch, self.thrust) = (0, 0, 0)
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
		
    # TODO: FIFO
    def respondRPLidar(self):
        # data = self.topics[constants.RPLIDAR_TOPIC]
        fifo = open(path, os.O_RDONLY)
        for line in fifo:
            print line
        fifo.close()
#        roll = 0
#        pitch = 0
#        min_distance = MAX_DISTANCE
#        angle = -1
#        for datapoint in data:
#            if datapoint.valid:
#                if (min_distance > datapoint.distance):
#                    min_distance = datapoint.distance
#                    angle = datapoint.angle

#        if (angle >= 0):
#            speed = BASE_SPEED
#            pitch = int(-speed * math.cos(angle))
#            roll = int(-speed * math.sin(angle))
#        else:
#             (roll, pitch) = (0, 0)
#        self.roll = roll
#        self.pitch = pitch

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
