from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class DialogServer(object):
    """docstring for Dialogself.Server"""
    def __init__(self, PORT):
               
        self.HOST = "127.0.0.1"
        self.PORT = PORT

        self.addresses = {}
        self.clients = {}

    def Connections(self):
        while True:
            client, addr = self.server.accept()
            print("{} is connected!!".format(addr))
            client.send(("Welcome to Chat Room. Type {quit} to exit. Enter your name: ").encode("utf-8"))
            self.addresses[client] = addr
            Thread(target = ClientConnection, args=(client, )).start()

    def ClientConnection(self, client):
        name = client.recv(BufferSize).decode("utf-8")
        client.send(("Hello {}".format(name)).encode("utf-8"))
        message = ("{} has joined the chat..").format(name)
        Broadcast(message.encode("utf-8"))
        self.clients[client] = name
        while True:
            msg = client.recv(BufferSize).decode("utf-8")
            if msg != "quit":
                Broadcast(msg.encode("utf-8"), name + ": ")
            else:
                message = ("{} has left the chat.").format(self.clients[client])
                Broadcast(message.encode("utf-8"))
                client.send(("Will see you soon..").encode("utf-8"))
                del self.clients[client]
                break

    def Broadcast(self, msg, name = ""):
        for sockets in self.clients:
            sockets.send(name.encode("utf-8") + msg)

    def serverRun(self):
        self.server = socket(family=AF_INET, type=SOCK_STREAM)
        # try:
        self.server.bind((self.HOST, self.PORT))
        # except OSError:
        #     print("self.Server Busy")
        BufferSize = 1024

        self.server.listen(5)
        print("Waiting for Connections... ")
        AcceptThread = Thread(target=self.Connections)
        AcceptThread.start()
        AcceptThread.join()
        self.server.close()


if __name__ == '__main__':
    gs = DialogServer(14441)
    gs.serverRun()