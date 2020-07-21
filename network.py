import socket
import pickle
from consoleapp.player import Player

class PlayerList():
    def __init__(self, players):
        self.players = players

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)
        self.player = pickle.loads(self.client.recv(2048))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            try:
                return pickle.loads(self.client.recv(2048))
            except:
                print('Got nothing for data sent')
        except:
            print('Sorry, there was an error in connecting to the server.')
