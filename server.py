import socket
from _thread import *
from board import Board
import pickle

server = '172.21.112.1'
port = 1234


id_count = 0


socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_obj.bind((server, port))
except socket.error as err:
    print(err)

socket_obj.listen(2)

print('Waiting for a connection, Server Started!\n')

game = Board()


def threaded_client(conn, current_player):
    global id_count
    conn.send(str.encode(str(current_player)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            else:
                if data != 'get':
                    pass
                    # Make a move on the board

                reply = game
                conn.sendall(pickle.dumps(game))

        except:
            break

    conn.close()


while True:
    conn, addr = socket_obj.accept()
    print('Connected to: ', addr)

    id_count += 1
    p = 'w'

    if id_count % 2 == 0:
        game.ready = True
        p = 'b'

    start_new_thread(threaded_client, (conn, p))
