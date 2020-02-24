import time
import zmq
import sys
import random
import numpy as np
import json
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray

def otsu():
    
    context = zmq.Context()
    Ostu_id = int(sys.argv[1])
    portpull = sys.argv[2]
    portpush = sys.argv[3]
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
        image = np.copy(work['img'])
        thresh = threshold_otsu(rgb2gray(image))
        work['img'] = (image > thresh).tolist()
        otsu_sender.send_json(work)
    otsu_sender.send_json(work)

otsu()