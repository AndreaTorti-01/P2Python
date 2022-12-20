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

def acceptF_t():
    global connectSocket
    # wait for connection
    connectSocket, addr = acceptSocket.accept()
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

symmetric_key = Fernet.generate_key()

UPnPt = forwardPort(PORT, PORT, None, None, False,
                    'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports opened successfully')

acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acceptSocket.bind((HOST, PORT))
acceptSocket.listen()
connectSocket = socket.socket
t = Thread(target=lambda: acceptF_t())
t.daemon = True
t.start()
print("server ready!")

external_ip = requests.get(
    'https://v4.ident.me/').text

window = tk.Tk()
frame1 = tk.Frame(
    window,
    bg=PALETTE["bg"]
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
window.configure(bg=PALETTE["bg"])
window.title('P2Python')

ip = tk.Label(
    window,
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    font="Consolas 14",
    text=f"Your Ip : {external_ip}"
)

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
    command=lambda: connectSocket.sendall(message.get().encode()) # type: ignore
)

ip.pack()
textInput.pack(side='left')
sendText.pack(side='left')
frame1.pack()

window.mainloop()

UPnPt = forwardPort(PORT, PORT, None, None, True,
                    'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports closed successfully')
