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

    def get_open_card(self):
        return self.deckobj.discard_pile[-1]

    def connect(self):
        self.client.connect(self.addr)
        with open('players.dat', 'rb') as f:
            self.players = pickle.loads(f.read())
        self.id, self.deckobj = pickle.loads(self.client.recv(2048))
        self.player = self.players[self.id]

    def send(self, data):
        self.client.send(pickle.dumps(data))

    def get_data(self):
        return pickle.loads(self.client.recv(2048))
