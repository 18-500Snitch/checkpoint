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


class ArduinoNode:
    def __init__(self, topics):
        self.topics = topics
        self.incoming = [(100,100), "0,0,0,0\n"]
        initPyserial(self.incoming)

    def loop(self):
        pwmArray = self.topics[constants.QUAD_TOPIC]
        msg = str(pwmArray[0])+","+str(pwmArray[1])+","+str(pwmArray[2])+","+str(pwmArray[3])+"\n"
        self.incoming[constants.STDOUT_INDEX] = msg

        rangefinder = self.incoming[constants.STDIN_INDEX]
        self.topics[constants.RANGEFINDER_TOPIC] = rangefinder


# input in format <string>\n
# puts ast.literal_eval(string) into incoming[0] if it does not begin with DEBUG:
def initPyserial(incoming):
    ser = serial.Serial('/dev/ttyUSB1') #open serial port
    print ser.name
    threading.Thread(target=serial_watcher, name='serial-watcher', args=[incoming,ser]).start()

# seperate thread
def serial_watcher(incoming,ser):
    try:
        while True: # constant loop
            string = ""
            while True: # single line
                # print("arduino iter")
                c = ser.read()
                if (c!=b'\n' and c!=b'\r'):
                    c = str(c)
                    string += str(c)
                else:
                    # print ("string:", string)
                    if (string != "" and not(string.startswith("DEBUG:"))):
                        result = "(100,100)"
                        try:
                            print string
                            result = ast.literal_eval(string)
                            incoming[constants.STDIN_INDEX] = result
                        finally: 
                            print "arduino finally"
                        print "arduino out"
                    break;
                time.sleep(constants.FREQUENCY)
    finally:
        ser.close()
