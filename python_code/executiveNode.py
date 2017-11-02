# DONE: stub
# TODO: implement
# TODO: test

import constants
import udpReceiver
from threading import Thread
import time

TIME_ZERO    = 0
TIME_STANDBY = TIME_ZERO    +  1000
TIME_ARM     = TIME_STANDBY +  7000
TIME_HOVER   = TIME_ARM     + 10000
TIME_DISARM  = TIME_HOVER   +  1000
TIME_END     = TIME_DISARM  +  1000

class ExecutiveNode:
    def __init__(self, topics):
        self.topics = topics
        self.behavior = constants.BEHAVIOR_RESTING
        self.lastMillis = constants.millis()
        self.startMillis = self.lastMillis
        self.incoming = [constants.BEHAVIOR_RESTING]
        # thread = Thread(target=udpReceiver.runCVReceiver, args = self.incoming)
        # thread.start()

    def loop(self):
        command = self.checkWifi()
        if (command == constants.BEHAVIOR_NULL):
            if (constants.millis() > self.lastMillis+2500):
                self.behavior = constants.BEHAVIOR_RESTING
        else:
            self.behavior = command

        self.topics[constants.BEHAVIOR_TOPIC] = self.behavior

    def checkWifi(self):
        if constants.millis() < self.startMillis + TIME_ZERO:
            return constants.BEHAVIOR_OFF
        if constants.millis() < self.startMillis + TIME_STANDBY:
            return constants.BEHAVIOR_OFF
        elif constants.millis() < self.startMillis + TIME_ARM:
            return constants.BEHAVIOR_ARM
        elif constants.millis() < self.startMillis + TIME_HOVER:
            return constants.BEHAVIOR_HOVER
        elif constants.millis() < self.startMillis + TIME_DISARM:
            return constants.BEHAVIOR_DISARM
        elif constants.millis() < self.startMillis + TIME_END:
            return constants.BEHAVIOR_OFF
        else: # should not get here
            return constants.BEHAVIOR_OFF
        # result = self.incoming[constants.STDIN]
        # self.incoming[constants.STDIN] = constants.BEHAVIOR_NULL
        # return result
