# source: https://wiki.python.org/moin/UdpCommunication
# usage: start node
#        


import socket
import ast

# TODO: implement node that calls runCVReceiver() and then spins

def runTCPReceiver():
  
  TCP_IP = "0.0.0.0"
  TCP_PORT = 5005

  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
  sock.bind((TCP_IP, TCP_PORT))
  sock.listen(1)

  print "setup done: Socket on 5005"
  conn,addr = sock.accept()

  while True:
    data = conn.recv(1024) # buffer size is 1024 bytes
    doWithData(data)

def doWithData(message):
  try:
    print "received message:", message
  finally:
    pass

# for testing (delete after implementing node)
runTCPReceiver()
