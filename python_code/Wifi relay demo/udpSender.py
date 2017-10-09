#source: https://wiki.python.org/moin/UdpCommunication

import socket

# number of relevant objects detected by camera
# data of quad first
# format [(x_coord,y_coord,z_coord,priority),(x_coord,y_coord,z_coord,priority)]
def sendUdp(coordinates):

  UDP_IP = "127.0.0.1"
  UDP_PORT = 5005
  
  print "UDP target IP:", UDP_IP
  print "UDP target port:", UDP_PORT
  
  message = str(coordinates)
  print "message:", message

  sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
  sock.sendto(message, (UDP_IP, UDP_PORT))

sendUdp([(1,2,3,4),(5,6,7,8)])
