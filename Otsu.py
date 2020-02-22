import time
import zmq
import sys
import random
import numpy as np
from skimage.filters import threshold_otsu

def otsu():
    
    context = zmq.Context()
    portpull = sys.argv[1]
    portpush = sys.argv[2]
    # recieve work
    otsu_receiver = context.socket(zmq.PULL)
    otsu_receiver.connect("tcp://127.0.0.1:%s" % portpull)
    # send work
    otsu_sender = context.socket(zmq.PUSH)
    otsu_sender.connect("tcp://127.0.0.1:%s" % portpush)
    
    while True:
        work = otsu_receiver.recv_json()
        if(work['frame_number'] == -1):
            break
        image = np.copy(work['img'])
        thresh = threshold_otsu(image)
        work['img'] = image > thresh
        otsu_sender.send_json(work)
    otsu_sender.send_json(work)

otsu()