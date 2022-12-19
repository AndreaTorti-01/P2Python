import urllib.request
import tkinter as tk
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from threading import Thread
import socket
from portforwardlib import forwardPort
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
import sys

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
otherPublic = public_key
HOST = "0.0.0.0"
PORT = 21763

public_key_b: bytes = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

UPnPt = forwardPort(PORT, PORT, None, None, False, 'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports opened successfully')


def connectF(friendip_s: str):
    t = Thread(target=lambda: connectF_t(friendip_s))
    t.daemon = True
    t.start()
def connectF_t(friendip_s: str):
    connectSocket.connect((friendip_s, PORT))
    print("connected!")
    connectSocket.sendall(public_key_b)
    otherPublic_b_enc: bytes = connectSocket.recv(2048)
    otherPublic_b: bytes = private_key.decrypt(
        otherPublic_b_enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    otherPublic: rsa.RSAPublicKey = load_pem_public_key(otherPublic_b)
    print("keys exchanged!")
    print(public_key, otherPublic)

def acceptF():
    t = Thread(target=lambda: acceptF_t())
    t.daemon = True
    t.start()
    print("server ready!")
def acceptF_t():
    connectSocket, addr = acceptSocket.accept()
    print(addr, "connected")
    otherPublic_b: bytes = connectSocket.recv(2048)
    otherPublic: rsa.RSAPublicKey = load_pem_public_key(otherPublic_b)

    public_key_b_enc: bytes = otherPublic.encrypt(
        public_key_b,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    print(sys.getsizeof(public_key_b_enc))
    connectSocket.sendall(public_key_b_enc)
    print("keys exchanged!")
    print(public_key, otherPublic)

acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acceptSocket.bind((HOST, PORT))
acceptSocket.listen()
acceptF()

palette = {
    "bg": "#4a4d4d",
    "fg": "#ffffff",
    "activebackground": "#656868",
    "activeforeground": "#ffffff"
}

external_ip = urllib.request.urlopen(
    'https://v4.ident.me/').read().decode('utf8')

window = tk.Tk()
frame1 = tk.Frame(
    window,
    bg=palette["bg"]
)

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
window.configure(bg=palette["bg"])
window.title('P2Python')

ip = tk.Label(
    window,
    bg=palette["bg"],
    fg=palette["fg"],
    font="Consolas 14",
    text=f"Your Socket-> {external_ip}:{acceptSocket.getsockname()[1]}"
)

friendip = tk.StringVar(window)
friend = tk.Entry(
    frame1,
    bg=palette["bg"],
    fg=palette["fg"],
    font="Consolas 14",
    width=15,
    textvariable=friendip
)

connect = tk.Button(
    frame1,
    text="Connect",
    font="Consolas 14",
    bg=palette["bg"],
    fg=palette["fg"],
    activebackground=palette["activebackground"],
    activeforeground=palette["activeforeground"],
    command=lambda: connectF_t(friendip.get())
)

ip.pack()
friend.pack(side="left")
connect.pack(side="left")
frame1.pack()
window.mainloop()

UPnPt = forwardPort(PORT, PORT, None, None, True, 'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports closed successfully')