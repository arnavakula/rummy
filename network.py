import socket
import pickle
from consoleapp.player import Player

class Network:
    def __init__(self, num):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.players = self.connect(num)

    def connect(self, num):
        self.client.connect(self.addr)
        self.deckobj = pickle.loads(self.client.recv(2048))
        pl = []
        for x in range(num):
            pl.append(Player(self.deckobj))
        self.client.send(pickle.dumps(self.deckobj))
        return pl

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            try:
                return pickle.loads(self.client.recv(2048))
            except:
                print('Got nothing for data sent')
        except:
            print('Sorry, there was an error in connecting to the server.')

n = Network(2)
