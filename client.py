import socket
import pickle


host = 'localhost'
port = 5555
lst = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

d = {1: 'hi', 2: 'there'}
s.send(pickle.dumps(d))

while True:
    data = pickle.loads(s.recv(2048))
    print('Received: {}'.format(data))
    lst.append(data)

print(lst)
