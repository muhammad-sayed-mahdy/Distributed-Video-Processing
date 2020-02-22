# Distributed-Video-Processing

A small program that distribute processing of videos among different machines.  
Processing of videos consists of thresholding using otsu then finding contours.  
The distribution is done on 2 different machines for simplicity of running,  
but it can be done on several machines by changing the ip addresses of machines

## Required Packages
* `numpy`
* `opencv`
* `pyzmq`
  
## How to run
`python machine1.py <input_file_name> <number_of_consumers> <machine1_ip_address>`  
`python machine2.py <output_file_name> <number_of_consumers> <machine1_ip_address>`

## Machine 1
It takes as input: name of the input video file, number of consumers that do Otsu
and ip address of this machine.  
It contains $1$ producer, $N$ consumers and $\lceil N/2 \rceil$ collectors.

1. ### Producer
    Takes a video as input and extracts frames from it, then sends the frames to the consumers.

2. ### Otsu Consumer
    Receives frames from producers and performs Otsu operation for thresholding,  
    then sends the thresholded images to the intermediate collectors.

3. ### Intermediate Collectors
    Each collector receives thresholded frames from 2 consumers and send them to 2 other consumers.

## Machine 2
It contains $N$ consumers and $1$ final collector.

1. ### Contours Consumer
   Receives frames from the intermediate collectors, performs contours finding  
   and sends them to the final collector.

2. ### Final Collector
   Receives frames from the contours consumers and append them to a list,  
   then sorts this list by frame number and write the list in a file