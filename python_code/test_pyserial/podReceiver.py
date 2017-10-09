# author: andrewzhang100@gmail.com
# reference material: pyserial.readthedocs.io/en/latest/shortintro.html

import serial
import ast

# input in format <string>\n
# calls "doWith(string) on each line
def runPodReceiver():
    ser = serial.Serial('/dev/ttyUSB0') #open serial port
    print(ser.name)
    ser.write(b'hello')
    try:
        while True: # constant loop
            string = ""
            while True: # single line
                c = ser.read()
                if (c!=b'\n' and c!=b'\r'):
                    c = str(c)[2]
                    string += str(c)
                else:
                    # print ("string:", string)
                    if (string != "" and string != "Out of range"):
                        doWith (string)
                    break;
    finally:
        ser.close()

def doWith(msg):
    # print ("doWith("+msg+")")
    try:
        result = ast.literal_eval(msg)
        print("result:", result)
    finally:
        pass

#for testing (delete after implementing node)
print("start program")
runPodReceiver()
