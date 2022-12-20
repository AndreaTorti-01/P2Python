import sys
import tkinter as tk
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from threading import Thread
import socket
from cryptography.fernet import Fernet
from portforwardlib import forwardPort
import requests

HOST = "0.0.0.0"
PORT = 21763
PALETTE = {
    "bg": "#4a4d4d",
    "fg": "#ffffff",
    "activebackground": "#656868",
    "activeforeground": "#ffffff"
}


class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see("end")  # scroll to the end

    def flush(self):  # needed for file like object
        pass

def send_message(msg: str):
    connectSocket.sendall(fernet.encrypt(msg.encode()))

def recv_message():
    while True:
        data_e = connectSocket.recv(4096)
        data = fernet.decrypt(data_e)
        print("received", data.decode())


def acceptF_t():
    global connectSocket
    # wait for connection
    connectSocket_tmp, addr = acceptSocket.accept()
    connectSocket = connectSocket_tmp
    print(addr, "connected")

    # receive public key and deserialize it
    otherPublic_b: bytes = connectSocket.recv(4096)
    otherPublic: rsa.RSAPublicKey = serialization.load_pem_public_key(
        otherPublic_b)  # type:ignore

    # encrypt symmetric key and send it
    symmetric_key_encr = otherPublic.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    connectSocket.sendall(symmetric_key_encr)
    print("keys exchanged!")
    t = Thread(target=recv_message)
    t.daemon = True
    t.start()


window = tk.Tk()
text = tk.Text(
    window,
    font="Consolas 14",
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
)
sys.stdout = TextRedirector(text, "stdout")
frame1 = tk.Frame(
    window,
    bg=PALETTE["bg"]
)

print("Welcome to P2Python!")
symmetric_key = Fernet.generate_key()
fernet = Fernet(symmetric_key)

UPnPt = forwardPort(PORT, PORT, None, None, False,
                    'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('Port opened successfully')
external_ip = requests.get(
    'https://v4.ident.me/').text

acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acceptSocket.bind((HOST, PORT))
acceptSocket.listen()
t = Thread(target=lambda: acceptF_t())
t.daemon = True
t.start()
print(f"Server ready, listening on IP {external_ip}")

# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = int(screen_width/2)
window_height = int(screen_height/2)

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.configure(bg=PALETTE["bg"])
window.title('P2Python')

message = tk.StringVar(window)
textInput = tk.Entry(
    frame1,
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    font="Consolas 14",
    width=15,
    textvariable=message
)

sendText = tk.Button(
    frame1,
    text="Send!",
    font="Consolas 14",
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    activebackground=PALETTE["activebackground"],
    activeforeground=PALETTE["activeforeground"],
    command=lambda: send_message(message.get())
)


textInput.pack(side='left')
sendText.pack(side='left')
frame1.pack()

text.pack()

window.mainloop()

UPnPt = forwardPort(PORT, PORT, None, None, True,
                    'TCP', 0, 'P2Python UPnP', False)
