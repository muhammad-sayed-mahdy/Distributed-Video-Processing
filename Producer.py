import time
import sys
import zmq
import numpy as np
import cv2

def producer():
    context = zmq.Context()
    port = sys.argv[1]
    videopath = sys.argv[2]
    N = sys.argv[3]
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:%s" % port)
    # Start your result manager and workers before you start your producers
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        work_message = {'frame_number': i, 'img': frame}
        zmq_socket.send_json(work_message)
    work_message = {'frame_number': -1, 'img': frame}
    for i in range(N):
        zmq_socket.send_json(work_message)

producer()
