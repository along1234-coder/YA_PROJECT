import random
import time
from select import select
import socket
from datetime import datetime
import pickle
import threading
from socket import *


class Room:

    def __init__(self, x, y, conditions, price_per_day):
        self.x = x
        self.y = y
        self.images = []
        self.conditions = conditions
        self.price_per_day = price_per_day


class Server:

    def __init__(self):

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(('127.0.0.1', 50000))
        self.server.listen(2)
        self.main_socks = [self.server]
        self.read_sockets = []
        self.write_sockets = []
        self._BUFFER = 1024
        self._PORT = 50000
        self._rooms = {12: True, 13: False}
        self.read_sockets += self.main_socks

    def run(self):

        while 1:

            readables, writeables, exceptions = select(self.read_sockets, self.write_sockets, [], 0)

            for sock in readables:
                if sock in self.main_socks:

                    # accepting new clients to the server
                    newsock, address = sock.accept()
                    newsock.send(pickle.dumps(self._rooms))
                    self.read_sockets.append(newsock)

                else:
                    data = sock.recv(self._BUFFER).decode()
                    if self._rooms[int(data)]:
                        sock.send(f"CLIENT chose room {int(data)}. That room is taken".encode())
                    else:
                        sock.send(f"CLIENT chose room {int(data)}. That room is not taken".encode())

    def addroom(self, room):
        self.__rooms[room[0]] = room[1]

    def getrooms(self):
        print(self.__rooms)


print("----SERVER STARTING----")
s = Server()
s.run()
print('DONE, LISTENING')
