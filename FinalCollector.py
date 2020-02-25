import time
import zmq
import pprint
import numpy as np
import sys
import json

def final_collector():
    if (len(sys.argv) < 2):
        print ("missing argument: output_file_name")
        return
    output_file = sys.argv[1]
    
    if (len(sys.argv) < 3):
        print ("missing argument: number_of_consumers")
        return
    N = int(sys.argv[2])

    if (len(sys.argv) < 4):
        print ("missing argument: port_number")
        return
    port_num = sys.argv[3]

    print ("Final Collector is on")

    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://127.0.0.1:" + port_num)
    collector_data = []
    cnt = 0
    while cnt < N:
        result = results_receiver.recv_json()
        if (result['frame_number'] == -1):
           cnt += 1
        else: 
            collector_data.append(result)

    collector_data.sort(key=lambda frame: frame['frame_number'])
    with open(output_file, "w") as file:
        json.dump(collector_data, file, indent=4)
    print ("Final Collector is done")

final_collector()