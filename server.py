import socket
import pickle
from _thread import *

host = 'localhost'
port = 5555
lst = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print('Waiting for connection...')

s.listen()

def threaded_client(conn):
    while True:
        try:
            value, suit = pickle.loads(conn.recv(2048))

            if not data:
                print('No connection')
                break
            else:
                print('Received: {}'.format(data))
        except:
            print('Lost connection')
            conn.close()
            break

#TODO implement some condition
while True:
    conn, addr = s.accept()
    start_new_thread(threaded_client, (conn,))
