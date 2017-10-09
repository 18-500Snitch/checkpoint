# DONE: stub
# DONE: implement
# TODO: test

import constants
import math

HOVER_CONSTANT = 100 # the value at which the quad is barely hovering
BASE_SPEED = 100000 # ele/til = BASE_SPEED/min_distance

# finished implementation
# not tested
class ControlNode:
    def __init__(self, topics):
        self.topics = topics
        (self.x, self.y, self.z) = (0, 0, 0)

    def loop(self):
        (x,y,z) = (0,0,0)
        rplidar = (self.topics[constants.RANGEFINDER_TOPIC][0] + self.topics[constants.RANGEFINDER_TOPIC][1])/2
        if   self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_OFF:
            pass
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_HOVER:
            (x, y) = self.respondRPLidar(self.topics[constants.RPLIDAR_TOPIC])
            z = 100 - rplidar
            z = z + HOVER_CONSTANT
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RESTING:
            if (rplidar < 10):
                z = 0
            elif (rplidar > 10):
                z = 10 - rplidar
                z = z + HOVER_CONSTANT
        elif self.topics[constants.BEHAVIOR_TOPIC] == constants.BEHAVIOR_RANDOM:
            assert False # not yet implemented
        else:
            assert False

        self.topics[constants.QUAD_TOPIC] = self.filter(x, y, z)

    @staticmethod
    def respondRPLidar(data):

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

        return x, y

    @staticmethod
    def filter( x, y, z):
        if x > 100: x = 100
        if x < -100: x = -100

        if y > 100: y = 100
        if y < -100: y = -100

        if z > 200: z = 200

        return x, y, z, 0
