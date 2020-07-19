import socket
import pickle


host = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

d = {1: 'how', 2: 'are', 3: 'you'}
s.send(pickle.dumps(d))
print(pickle.loads(s.recv(2048)))
