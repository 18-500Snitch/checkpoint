# author: andrewzhang100@gmail.com
# advisor: shapecaster@outlook.com

# DONE: stub
# TODO: implement
# TODO: test

import constants
import subprocess
from threading import Thread
import ast
import sys
import time
import Queue

ANGULAR_OFFSET = 135 # anglular offset of rplidar


class RPLidarNode:
    def __init__(self, topics):
        self.topics = topics

        self.incoming = [[(0,0,0)]]

        self.proc = subprocess.Popen("$HOME/checkpoint/rplidar_sdk/output/Linux/Release/ultra_simple 8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        self.dataQueue = Queue.Queue()
        thread = Thread(target=self.stream_watcher, name='stdout-watcher', args=('STDOUT', self.proc.stdout))
        thread.daemon = True
        thread.start()

    def loop(self):
        try:
            data = self.dataQueue.get(block=False) #self.getRPLidarData()
            newData = []

            for datapoint in data:
                newData.append(constants.RPLidarDatapoint(datapoint[0],(datapoint[1]+ANGULAR_OFFSET)%360,datapoint[2]))

            self.topics[constants.RPLIDAR_TOPIC] = newData
        except Queue.Empty:
            pass

    def getRPLidarData(self):
        # TODO: implement
        # msg = sys.stdin.read(1)
        return self.incoming[constants.STDIN_INDEX]
    
    # seperate thread
    def stream_watcher(self, identifier,stream):
        for line in iter(stream.readline,""):
            try:
                if (line.startswith("[")):
                    msg = ast.literal_eval(line)
                    #self.incoming[constants.STDIN_INDEX] = msg
                    self.dataQueue.put(item=msg,block=False)
            finally:
                #time.sleep(constants.FREQUENCY)
                pass
        if not stream.closed:
            stream.close()


