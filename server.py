import socket
from _thread import *
import sys

def read_pos(s):
    s = s.split(',')
    return int(s[0]), int(s[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print('Waiting for a connection, server started')

#p1, p2
pos = [(0, 0), (100, 100)]

def threaded_client(conn, current_player):
    #first, send start_pos
    conn.send(str.encode(make_pos(pos[current_player])))

    reply = ''
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            print('SERVER RECV DATA BELOW')
            print(data)
            pos[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                if current_player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print('Received {}'.format(data))
                print('Sending {}'.format(reply))
                conn.sendall(str.encode(make_pos(reply)))

            conn.sendall(str.encode(reply))
        except:
            break

            print('lost connection')
            conn.close()

current_player = 0
while True:
    conn, addr = s.accept()
    print('Connected to {}'.format(addr))

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
