import pickle
import time
from socket import *
import threading
from tkinter import *
import registration_form


class Client:

    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self._BUFFER = 1024
        self._ADDR = ('127.0.0.1', 50000)

    def recieve(self):

        while 1:

            data = self.client.recv(self._BUFFER)
            if not data:
                break
            try:
                print(data.decode())
            except:
                print(pickle.loads(data))

    def connect(self):

        self.client.connect(self._ADDR)
        threading.Thread(target=self.recieve).start()
        threading.Thread(target=self.send).start()

    def send(self):

        while True:
            data = input("SEND ROOM >>> ")
            self.client.send(data.encode())
            if not data:
                break

    def add(self, place, cord):
        self.client.send(pickle.dumps([place, cord]))

if __name__ == "__main__":
    print("----STARTING CONNECTION WITH SERVER---")
    c = Client()
    c.connect()