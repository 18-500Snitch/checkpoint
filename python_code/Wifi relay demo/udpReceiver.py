# source: https://wiki.python.org/moin/UdpCommunication
# usage: start node
#        


import socket
import ast

# TODO: implement node that calls runCVReceiver() and then spins

def runCVReceiver():
  
  UDP_IP = "0.0.0.0"
  UDP_PORT = 5005

  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))

  print "setup done: Socket on 5005"
  
  while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    doWithCV(data)

def doWithCV(message):
  try:
    print "received message:", message
  finally:
    pass

# for testing (delete after implementing node)
runCVReceiver()
