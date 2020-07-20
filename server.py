import socket
import pickle
from _thread import *
from consoleapp.cards import *

host = 'localhost'
port = 5555

deckobj = Deck()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print('Waiting for connection...')

s.listen()

def threaded_client(conn):
    #send initial deck
    global deckobj
    conn.send(pickle.dumps(deckobj))
    deckobj = pickle.loads(conn.recv(2048))
    print(len(deckobj.deck))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print('No connection')
                break
            else:
                print('Received: {}'.format(data))
                conn.send(pickle.dumps(deckobj))
        except:
            print('Lost connection')
            conn.close()
            break

#TODO implement some condition
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn,))
