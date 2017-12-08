# author: andrewzhang100@gmail.com
# reference material: pyserial.readthedocs.io/en/latest/shortintro.html

# DONE: stub
# TODO: implement
# TODO: test

import constants
import serial
import threading
import ast
import time

DEFAULT_RANGEFINDER     =  (400,400) # maximum range of rangefinder
DEFAULT_RANGEFINDER_STR = "(400,400)" # maximum range of rangefinder


class ArduinoNode:
    def __init__(self, topics):
        self.topics = topics
        self.incoming = [DEFAULT_RANGEFINDER]
        self.ser = serial.Serial('/dev/arduino') # open serial port
        thread = threading.Thread(target=serialWatcher, name='serial-watcher', args=[self.ser, self.incoming])
        thread.daemon = True
        thread.start()

    def loop(self):
        # send pwm output
        pwmArray = self.topics[constants.QUAD_TOPIC]
        msg = str(pwmArray[0])+","+str(pwmArray[1])+","+str(self.topics[constants.THRUST_TOPIC])+","+str(pwmArray[2])+"\n"
#        msg = "0,0,-5,98\n"
        print(msg)
        self.ser.write(msg)
        # recieve input
        rangefinder = self.incoming[constants.STDIN_INDEX]
        self.topics[constants.RANGEFINDER_TOPIC] = rangefinder

# input in format <string>\n
# puts ast.literal_eval(string) into incoming[0] if it does not begin with DEBUG:
# seperate thread
def serialWatcher(ser, incoming):
    string = ""
    while True: # constant loop
        # read serial
        c = ser.read(size=1)
        if (c!=b'\n' and c!=b'\r'): 
            string += str(c) # add stuff
        else: # now that the line has been completely sent
            processSerial(incoming, string)
            string = ""
    ser.close()

def processSerial(incoming, string):
    if string == "": return
    if not(string.startswith(">")): return
    string = string.split(">",1)[1] # starting character
    if string == "": return
    if string.startswith("(") and string.endswith(")"):
        result = string
        incoming[constants.STDIN_INDEX] = ast.literal_eval(string)

