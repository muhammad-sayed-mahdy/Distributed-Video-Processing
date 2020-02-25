import time
import zmq
import pprint
import sys
import cv2
import json


def collector1():

    collector_id = int(sys.argv[1])
    ip_address = sys.argv[2]
    portpull = sys.argv[3]
    portpush = sys.argv[4]
    context = zmq.Context()

    collector1_receiver = context.socket(zmq.PULL)
    collector1_receiver.bind("tcp://127.0.0.1:%s" % portpull)
    
    collector1_sender = context.socket(zmq.PUSH)
    collector1_sender.bind("tcp://%s:%s" % (ip_address, portpush)) 
   
    numberofconsumers = 0
    while True:
        result = collector1_receiver.recv_json()
        if(result['frame_number'] == -1):
            numberofconsumers += 1
        if(numberofconsumers == 2):
            break
        collector1_sender.send_json(result)
    collector1_sender.send_json(result)
    collector1_sender.send_json(result)

collector1()
