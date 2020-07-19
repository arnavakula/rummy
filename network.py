import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except:
            print('Sorry, there was an error in connecting to the server.')

# n = Network()
# n.send('connected to network class')
