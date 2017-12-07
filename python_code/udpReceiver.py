# source: https://wiki.python.org/moin/UdpCommunication
# usage: start node
#

import constants
import threading
import socket
import ast
import time


class UdpNode:
    def __init__(self, topics):
        self.topics = topics
        self.incoming = ["0\n"]
        UDP_IP = "0.0.0.0"
        UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        
        thread = threading.Thread(target=udpWatcher, name='udp-watcher', args=[self.sock, self.incoming])
        thread.daemon = True
        thread.start()

    def loop(self):
        # recieve input
        msg = self.incoming[constants.STDIN_INDEX]
        self.topics[constants.UDP_TOPIC] = msg


def udpWatcher(sock,incoming):
    
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if data:
            incoming[constants.STDIN_INDEX] = data
