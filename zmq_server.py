import json
import zmq
import time
from collections import OrderedDict
from type_def import *


def make_json():
    file_data = OrderedDict()
    file_data["map"] = maze_cell
    with open('test.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False)


def start_server(ip, port):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://{ip}:{port}")

    return socket


# msg = socket.recv()  # uncomment for Req/Rep
# socket.send_json(test.json)