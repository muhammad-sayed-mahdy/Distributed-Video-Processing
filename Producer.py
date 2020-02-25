import time
import sys
import zmq
import numpy as np
import cv2
import json

def producer():
    context = zmq.Context()
    port = sys.argv[3]
    videopath = sys.argv[1]
    N = int(sys.argv[2])
    print("Producer is On")
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:%s" % port)
    # Start your result manager and workers before you start your producers
    i = 0
    cap = cv2.VideoCapture(videopath)
    while(cap.isOpened() and i < 10):
        ret, frame = cap.read()
        work_message = json.dumps({'frame_number': i, 'img': frame.tolist()})
        zmq_socket.send_json(work_message)
        i += 1
    work_message = json.dumps({'frame_number': -1, 'img': frame.tolist()})
    for i in range(N):
        zmq_socket.send_json(work_message)
    print("Producer is done")

producer()
