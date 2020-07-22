import socket
import pickle
from _thread import *
from consoleapp.cards import *
from consoleapp.player import *

host = 'localhost'
port = 5555

deckobj = Deck()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print('Waiting for connection...')

s.listen()
players = []

class PlayerList():
    def __init__(self, players):
        self.players = players


#TODO except if too many players join server
for i in range(2):
    p = Player(deckobj)
    p.id = i
    players.append(p)

with open('players.dat', 'wb') as f:
    f.truncate(0)
    f.write(pickle.dumps(players))

def threaded_client(conn, player):
    #send id
    conn.send(str(player).encode())

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print('No connection')
                break
            else:
                print('Received: {}'.format(data))
                # conn.send
        except:
            print('Lost connection')
            conn.close()
            break

#TODO implement some condition
player = 0
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn, player))
    player += 1
