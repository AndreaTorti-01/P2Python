from threading import Thread
import socket

def connectF_t(friendip: str, connectSocket: socket.socket):
    t = Thread(target=lambda: connectF(friendip, connectSocket))
    t.daemon = True
    t.start()
def connectF(friendip, connectSocket):
    addr = friendip.get().split(":")
    port = int(addr[1])
    connectSocket.connect((addr[0], port))
    print("connected!")

def acceptF_t(acceptSocket: socket.socket):
    t = Thread(target=lambda: acceptF(acceptSocket))
    t.daemon = True
    t.start()
    print("server ready!")
def acceptF(acceptSocket):
    _, addr = acceptSocket.accept()
    print(addr, "connected")

def createSockets():
    HOST = "0.0.0.0"
    acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    acceptSocket.bind((HOST, 0))
    acceptSocket.listen()
    acceptF_t(acceptSocket)
    return acceptSocket, connectSocket