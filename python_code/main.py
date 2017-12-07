
# DONE: implement
# DONE: test

import rosLib

import constants

import executiveNode
import controlNode
# import rplidarNode
# import arduinoNode

topics = {constants.RPLIDAR_TOPIC:[],
          constants.QUAD_TOPIC:(0,0,0,0),
          constants.RANGEFINDER_TOPIC:(0,0),
          constants.BEHAVIOR_TOPIC:constants.BEHAVIOR_OFF}

nodes = [# arduinoNode.ArduinoNode(topics),
         controlNode.ControlNode(topics),
         executiveNode.ExecutiveNode(topics)]

master = rosLib.Master(nodes, topics)
master.run()
