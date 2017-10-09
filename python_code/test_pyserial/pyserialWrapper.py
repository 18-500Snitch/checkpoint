
import serial
from threading import Thread
import ast
import constants

# input in format <string>\n
# puts ast.literal_eval(string) into incoming[0] if it does not begin with DEBUG:

def initPyserial(incoming):
    ser = serial.Serial('/dev/ttyUSB1') #open serial port
    print ser.name
    Thread(target=serial_watcher, name='serial-watcher', args=[incoming,ser]).start()
        
def serial_watcher(incoming,ser):
    try:
        while True: # constant loop
            string = ""
            while True: # single line
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
                            pass
                    break;
    finally:
        ser.close()
