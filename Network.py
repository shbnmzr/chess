import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '172.21.112.1'
        self.port = 1234
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # only gets player number: 0 or 1
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            # Sends string to server
            self.client.send(str.encode(data))
            # Receives object data
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as err:
            print(err)
