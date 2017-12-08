# DONE: stub
# DONE: implement
# TODO: test

import constants
import math
import os
import sys
import re

# FIFO
PIPE_PATH = "/tmp/rplidar.fifo"
MAX_BUF = 4096

SAFE_BUF = 0.7 # The Distance that the quadcopter will start moving away from things 
META = 3 # number of rplidar data points that are not actual data
# finished implementation
# not tested
class ControlNode:
    def __init__(self, topics):
        self.armStatus = "DISARM"
        self.topics = topics
        # only want to create pipe once, should not assume which node creates first
        if not os.path.exists(PIPE_PATH):
            os.mkfifo(PIPE_PATH)

    def loop(self):
        command = self.topics[constants.UDP_TOPIC]
        arduRange = (self.topics[constants.RANGEFINDER_TOPIC][0] + self.topics[constants.RANGEFINDER_TOPIC][1])/2

        if self.string_found(constants.CMD_ARM, command):
            self.topics[constants.QUAD_TOPIC] = constants.ARM
            self.topics[constants.THRUST_TOPIC] = 900
            self.armStatus = "ARM"
        if self.string_found(constants.CMD_OFF, command):
            self.topics[constants.QUAD_TOPIC] = constants.OFF
            self.topics[constants.THRUST_TOPIC] = 800
        if self.string_found(constants.CMD_DISARM, command):
            self.topics[constants.QUAD_TOPIC] = constants.DISARM
            self.topics[constants.THRUST_TOPIC] = 900
            self.armStatus = "DISARM"
        if self.string_found(constants.CMD_FLOAT, command):
            self.topics[constants.QUAD_TOPIC] = constants.FLOAT
        if self.string_found(constants.CMD_FWD, command):
            self.topics[constants.QUAD_TOPIC] = constants.LEAN_FWD
        if self.string_found(constants.CMD_BCK, command):
            self.topics[constants.QUAD_TOPIC] = constants.LEAN_BCK
        if self.string_found(constants.CMD_LFT, command):
            self.topics[constants.QUAD_TOPIC] = constants.LEAN_LFT
        if self.string_found(constants.CMD_RHT, command):
            self.topics[constants.QUAD_TOPIC] = constants.LEAN_RHT
        if self.string_found(constants.CMD_RISE, command):
            self.topics[constants.THRUST_TOPIC] += constants.RISE
        if self.string_found(constants.CMD_DECEND, command):
            self.topics[constants.THRUST_TOPIC] -= constants.DECEND
		
    def respondRPLidar(self):
        # FIFO
        # read data from rplidar_ros through fifo
        fifo = os.open(PIPE_PATH, os.O_RDONLY)
        rplidar_str = os.read(fifo, MAX_BUF)
        os.close(fifo)
        # parse string into data
        rplidar_data = [float(data) for data in (rplidar_str.replace('\x00', '')).split()]
        (angle_min, angle_max, angle_inc) = rplidar_data[0:META]
        rplidar_data = rplidar_data[META:]
        index = int(round(angle_max / angle_inc))
        # find nearest distance and angle
        near_only = [(theta, d) for (d, theta) in 
            enumerate(rplidar_data) if(d > 0)]
        (min_dist, angle) = min(near_only) if(near_only != []) else (None, None)
        if(angle):
            angle = angle_min + (angle * angle_inc) # actual angle
            # update pitch and roll
            (self.pitch, self.roll) = (int(-BASE_SPEED * math.cos(angle)),
                int(-BASE_SPEED * math.sin(angle))) if(min_dist < SAFE_BUF) else (0, 0)

    def string_found(self, search_str, msg_str):
        if re.search(r"\b" + re.escape(search_str) + r"\b", msg_str):
            return True
        return False
