import socket
from _thread import *
import sys

server = '10.0.0.17'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print('Waiting for a connection, server started')

def threaded_client(conn):

    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                print('Disconnected')
                break
            else:
                print('Received {}'.format(reply))

            conn.sendall(str.encode(reply))
        except:
            break

while True:
    conn, addr = s.accept()
    print('Connected to {}'.format(addr))

    start_new_thread(threaded_client, (conn,))