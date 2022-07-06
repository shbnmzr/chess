"""
author: Shabnam Zare
email: shabnam.zare@yahoo.com
date: 7/4/2022
"""

import socket
import os
from dotenv import load_dotenv
import pygame

load_dotenv()


class Network:
    client_object = None
    player_color = None

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv('SERVER')
        self.port = int(os.getenv('PORT'))
        self.addr = (self.server, self.port)
        Network.client_object = self.client
        self.p = self.connect()
        Network.player_color = self.p
        if self.p == 'w':
            pygame.display.set_caption('Shabnam Zare -- WHITE')
        else:
            pygame.display.set_caption('Shabnam Zare -- BLACK')

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print('Something went wrong!')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as err:
            print(err)
