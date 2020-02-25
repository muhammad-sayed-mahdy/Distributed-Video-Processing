import sys
import os

if len(sys.argv) < 2:
    print("missing argument: output_file_name")
    exit()
output_file = sys.argv[1]

if len(sys.argv) < 3:
    print("missing argument: number_of_consumers")
    exit()
N = int(sys.argv[2])

if len(sys.argv) < 4:
    print("missing argument: machine1_ip_address")
    exit()
ip_address = sys.argv[3]

start_port = 5000
collectorsN = (N + 1) // 2  # int(ceil(N/2))
start_port += 1 + collectorsN  # producer & collectors ports in the 1st machine

collectors1_send_ports = range(start_port, start_port + collectorsN)
start_port += collectorsN

final_collector_port = start_port
start_port += 1

for i in range(N):
    # consumer_num, ip_address, receive_port_num, send_port_num
    os.system(
        "python ContoursConsumer.py {} {} {} {} &".format(
            i, ip_address, collectors1_send_ports[i // 2], final_collector_port
        )
    )
    print ("turning on ContoursConsumer #{} on".format(i));

os.system("python FinalCollector.py {} {} {} &".format(output_file, N, final_collector_port))
print ("turning on final collector");