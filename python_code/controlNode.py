# DONE: stub
# DONE: implement
# TODO: test

import constants
import math

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
        (self.x, self.y, self.z) = (0, 0, 0)

    def loop(self):
        (self.x,self.y,self.z) = (0,0,0)
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
            self.z = HOVER_CONSTANT-DROP_CONSTANT
            self.respondRPLidar()
            self.topics[constants.QUAD_TOPIC] = self.filter()
        elif command == constants.BEHAVIOR_RANDOM:
            assert False # not yet implemented
        elif command == constants.BEHAVIOR_NULL:
            assert False # should never happen
        else:
            assert False

    def respondRangefinder(self,arduRange,behavior):
        z = 0
        if behavior == constants.BEHAVIOR_HOVER:
            z = HOVER_HEIGHT - arduRange
            z = z + HOVER_CONSTANT
        elif behavior == constants.BEHAVIOR_RESTING:
            if (arduRange < 10):
                z = 0
            elif (arduRange > 10):
                z = HOVER_CONSTANT-DROP_CONSTANT
        else:
            assert False
        self.z = z
		
    def respondRPLidar(self):
        data = self.topics[constants.RPLIDAR_TOPIC]
        x = 0
        y = 0
        min_distance = MAX_DISTANCE
        angle = -1
        for datapoint in data:
            if datapoint.valid:
                if (min_distance > datapoint.distance):
                    min_distance = datapoint.distance
                    angle = datapoint.angle

        if (angle >= 0):
            speed = BASE_SPEED
            y = int(-speed * math.sin(angle))
            x = int(-speed * math.cos(angle))
        else:
             (x, y) = (0, 0)
        self.x = x
        self.y = y

    def filter(self):
        x = self.x
        y = self.y
        z = self.z
        if(abs(x) > abs(y) and abs(x) > 100):
            scaleFactor = abs(x) / 100
            x = x / scaleFactor
            y = y / scaleFactor
        elif(abs(x) < abs(y) and abs(y) > 100):
            scaleFactor = abs(y) / 100
            x = x / scaleFactor
            y = y / scaleFactor
        
        if z > 200: z = 200

        return x, y, z, 0
