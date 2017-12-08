
# DONE: implement
# DONE: test

import rosLib

import constants

import controlNode
import arduinoNode
import udpNode

topics = {constants.RPLIDAR_TOPIC:[],
          constants.QUAD_TOPIC:(0,0,0,0),
          constants.RANGEFINDER_TOPIC:(0,0),
          constants.UDP_TOPIC:[]}

nodes = [arduinoNode.ArduinoNode(topics),
         controlNode.ControlNode(topics),
         udpNode.UdpNode(topics)]

master = rosLib.Master(nodes, topics)
master.run()
