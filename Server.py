"""
author: Shabnam Zare
email: shabnam.zare@yahoo.com
date: 7/4/2022
"""

import socket
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SERVER')
port = int(str(os.getenv('PORT')))
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_obj.bind((server, port))
except socket.error as err:
    print(err)

socket_obj.listen(2)
currentTurn = 'w'
connections = []


def thread_client(connection):
    while True:
        data = connection.recv(1024 * 4)
        allowed_connections_to_send = filter(lambda x: x is not connection, connections)
        for conn in allowed_connections_to_send:
            conn.send(data)


print('Waiting for first player to connect')
first_player, first_player_address = socket_obj.accept()
first_player.send('w'.encode())
first_player_thread = Thread(target=thread_client, args=(first_player,))
connections.append(first_player)

print('Waiting for second player to connect')
second_player, second_player_address = socket_obj.accept()
second_player.send('b'.encode())
second_player_thread = Thread(target=thread_client, args=(second_player,))
connections.append(second_player)

print("[x] Game Started")

first_player_thread.start()
second_player_thread.start()
first_player_thread.join()
second_player_thread.join()
