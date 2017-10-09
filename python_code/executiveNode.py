# DONE: stub
# TODO: implement
# TODO: test

import constants
import udpReceiver
from threading import Thread
import time

class ExecutiveNode:
    def __init__(self, topics):
        self.topics = topics
        self.behavior = constants.BEHAVIOR_RESTING
        self.lastMillis = constants.millis()
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
        return constants.BEHAVIOR_HOVER
        # result = self.incoming[constants.STDIN]
        # self.incoming[constants.STDIN] = constants.BEHAVIOR_NULL
        # return result
