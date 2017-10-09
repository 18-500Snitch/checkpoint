# author: andrewzhang100@gmail.com
# original: pyserial.readthedocs.io/en/latest/shortintro.html
# reference material: 

import serial

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
                if (string != ""):
                    print (string)
                    break;
finally:
    ser.close()
