import sys
import zmq

ctx = zmq.Context()


def run_server(port, name):
    print("STARTING SERVER")
    sock = ctx.socket(zmq.REP)
    sock.bind(f'tcp://*:{port}')
    print("READY")
    while True:
        message = sock.recv_string()
        print(f'RECEIVED: {message}')
        print(f'SENDING:  {name},{message}')
        sock.send_string(','.join((name, message)))

        
def run_client(*ports):
    sock = ctx.socket(zmq.REQ)
    for port in ports:
        sock.connect(f'tcp://localhost:{port}')
    while True:
        line = input('>> ')
        print(f'SENDING: {line}')
        sock.send_string(line)
        rep = sock.recv_string()
        name, message = rep.split(',', 1)
        print(f'RECEIVED: {message} FROM {name}')
        if line == 'bye':
            break
    sock.close()