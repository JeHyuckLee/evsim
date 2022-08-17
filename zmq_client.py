# client

import zmq
import time
import sys

context = zmq.Context()

socket = context.socket(zmq.PULL)
#socket = context.socket(zmq.REQ)    # uncomment for Req/Rep

socket.connect("tcp://127.0.0.1:5555")

while True:
    #socket.send('')     # uncomment for Req/Rep
    message = socket.recv()
    for i in range(100):
        for j in range(100):
            print(message[j][i])
