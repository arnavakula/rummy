from network import Network
import time

def read_pos(s):
    s = s.split(',')
    return int(s[0]), int(s[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

def main():

    run = True
    n = Network()
    start_pos = read_pos(n.get_pos())
    print('START POS BELOW')
    print(start_pos)

    while run:
        #send p1 pos and get p2 pos
        time.sleep(10)
        p2_pos = read_pos(n.send(make_pos((start_pos[0], start_pos[1]))))
        print('P2 POS BELOW')
        print(p2_pos[0], p2_pos[1])
