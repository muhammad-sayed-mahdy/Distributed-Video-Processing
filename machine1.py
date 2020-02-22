import sys
import os

if len(sys.argv) < 2:
    print("missing argument: input_file_name")
    exit()
input_file = sys.argv[1]

if len(sys.argv) < 3:
    print("missing argument: number_of_consumers")
    exit()
N = int(sys.argv[2])

if len(sys.argv) < 4:
    print("missing argument: machine1_ip_address")
    exit()
ip_address = sys.argv[3]

start_port = 5000
producer_port_num = start_port
os.system("python Producer.py {} {} {}".format(input_file, N, producer_port_num))
start_port += 1

collectorsN = (N + 1) // 2  # int(ceil(N/2))
otsu_send_ports = range(start_port, start_port + collectorsN)
start_port += collectorsN

for i in range(N):
    # consumer_num, ip_address, receive_port_num, send_port_num
    os.system(
        "python Otsu.py {} {} {} {}".format(
            i, ip_address, producer_port_num, otsu_send_ports[i // 2]
        )
    )

collectors1_send_ports = range(start_port, start_port + collectorsN)
start_port += collectorsN
for i in range(collectorsN):
    # collector_num, receive_port_num, send_port_num
    os.system(
        "python Collector1.py {} {} {}".format(
            i, otsu_send_ports[i], collectors1_send_ports[i]
        )
    )

