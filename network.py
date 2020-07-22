import socket
import pickle
from consoleapp.player import Player

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)
        with open('players.dat', 'rb') as f:
            self.players = pickle.loads(f.read())
        self.id = int(self.client.recv(2048).decode())
        print(self.id)
        self.player = self.players[self.id]

    def send(self, data):
        self.client.send(pickle.dumps(data))

n = Network()
print(n.players)
print(n.player)
