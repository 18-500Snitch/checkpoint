# library

import constants
import time

class Master:
    def __init__(self, nodes, topics):
        self.nodes = nodes
        self.topics = topics
    def run(self):
        while True:
            for node in self.nodes:
                node.loop()
            print "[",constants.millis(),"]", self.topics
            time.sleep(constants.FREQUENCY)

"""
class Node:
    def __init__(self, topics):
        self.topics = topics
        self.output = output
        assert False

    def loop(self):
        pass
        assert False
"""
