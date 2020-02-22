import zmq
import sys
import cv2
import numpy as np

def contoursConsumer():
    if (len(sys.argv) < 2):
        print ("missing argument: consumer_number")
        return
    consumer_num = sys.argv[1]
    if (len(sys.argv) < 3):
        print ("missing argument: ip_address")
        return
    ip_address = sys.argv[2]
    if (len(sys.argv) < 4):
        print ("missing argument: receiver_port_number")
        return
    receiver_port_num = sys.argv[3]
    if (len(sys.argv) < 5):
        print ("missing argument: sender_port_number")
    sender_port_num = sys.argv[4]

    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://{}:{}".format(ip_address, receiver_port_num))
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:" + sender_port_num)
    
    while True:
        work = consumer_receiver.recv_json()
        if (work['frame_number'] == -1):
            break
        img = work['img']

        #cv2.imshow("received_frames", img)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        result = {'frame_number': work['frame_number'], 'contours' : contours, 'hierarchy' : hierarchy}
        consumer_sender.send_json(result)

    result = {'frame_number': -1}
    consumer_sender.send_json(result)

    #cv2.destroyAllWindows()

    print ("consumer #{} is done.".format(consumer_num))
contoursConsumer()