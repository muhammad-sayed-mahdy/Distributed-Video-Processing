import time
import zmq
import sys
import random
import numpy as np
import json
import cv2

def otsu():
    
    context = zmq.Context()
    Ostu_id = int(sys.argv[1])
    portpull = sys.argv[2]
    portpush = sys.argv[3]
    print ("Otsu #{} is on".format(Ostu_id))
    # recieve work
    otsu_receiver = context.socket(zmq.PULL)
    otsu_receiver.connect("tcp://127.0.0.1:%s" % portpull)
    # send work
    otsu_sender = context.socket(zmq.PUSH)
    otsu_sender.connect("tcp://127.0.0.1:%s" % portpush)
    
    while True:
        work = otsu_receiver.recv_json()
        work = json.loads(work)
        if(work['frame_number'] == -1):
            break
        img = np.array(work['img'])
        thres,image = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        work['img'] = image.tolist()
        otsu_sender.send_json(work)
    otsu_sender.send_json(work)
    print ("Otsu #{} is done".format(Ostu_id))

otsu()