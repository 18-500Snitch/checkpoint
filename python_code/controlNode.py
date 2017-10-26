# DONE: stub
# DONE: implement
# TODO: test

import constants
import math

HOVER_CONSTANT = 100 # the value at which the quad is barely hovering
HOVER_HEIGHT = 100
BASE_SPEED = 100000 # ele/til = BASE_SPEED/min_distance

# finished implementation
# not tested
class ControlNode:
    def __init__(self, topics):
        self.topics = topics
        (self.x, self.y, self.z) = (0, 0, 0)

    def loop(self):
        (self.x,self.y,self.z) = (0,0,0)
		
        arduRange = (self.topics[constants.RANGEFINDER_TOPIC][0] + self.topics[constants.RANGEFINDER_TOPIC][1])/2
        self.respondRangefinder(arduRange)
        self.respondRPLidar()

        self.topics[constants.QUAD_TOPIC] = self.filter()

    def respondRangefinder(self,arduRange):
        z = 0
        if self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_OFF:
            pass
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_HOVER:
            z = HOVER_HEIGHT - arduRange
            z = z + HOVER_CONSTANT
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RESTING:
            if (arduRange < 10):
                z = 0
            elif (arduRange > 10):
                z = 10 - arduRange
                z = z + HOVER_CONSTANT
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RANDOM:
            assert False # not yet implemented
        else:
            assert False
        self.z = z
		
    def respondRPLidar(self):
        data = self.topics[constants.RPLIDAR_TOPIC]
        x = 0
        y = 0
        if self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_OFF:
            pass
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_HOVER:
            min_distance = -1
            angle = -1
            for datapoint in data:
                if datapoint.valid:
                    if (min_distance == -1 or min_distance > datapoint.distance):
                        min_distance = datapoint.distance
                        angle = datapoint.angle

            if (angle >= 0):
                speed = BASE_SPEED / min_distance
                y = int(-speed * math.sin(angle))
                x = int(-speed * math.cos(angle))
            else:
                 (x, y) = (0, 0)
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RESTING:
            (x,y) = (0,0)
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RANDOM:
            assert False # not yet implemented
        else:
            assert False

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
