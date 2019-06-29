from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import time
class GroupClient:
    def __init__(self):

        self.HOST = "127.0.0.1"
        self.PORT = 3000
        self.BufferSize = 1024
        self.uname = ""


    def run(self, uname):
        self.client = socket(family=AF_INET, type=SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        self.RecieveThread = Thread(target=self.Recieve).start()
        self.SendThread = Thread(target=self.Send).start()
        self.uname = uname
        time.sleep(0.5)
        self.client.send(uname.encode("utf-8"))
        print("uname send : %s"%uname)

    def exit(self):
        self.client.close()
        del self


    def Recieve(self):
        while True:
            try:
                msg = self.client.recv(self.BufferSize).decode("utf-8")
                print(msg)
            except OSError:
                break

    def Send(self):
        # self.client.send(self.uname.encode("utf-8"))
        while True:
            msg = input()
            if msg == "quit":
                self.client.send(msg.encode("utf-8"))
                self.client.close()
                break
            else:
                self.client.send(msg.encode("utf-8"))


