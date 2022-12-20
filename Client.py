import sys
import tkinter as tk
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from threading import Thread
import socket
from cryptography.fernet import Fernet

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


def connectF(friendip_s: str):
    t = Thread(target=lambda: connectF_t(friendip_s))
    t.daemon = True
    t.start()


def connectF_t(friendip_s: str):
    # this will be the actual aes key
    global fernet

    # connect to friend
    connectSocket.connect((friendip_s, PORT))
    print("connected!")

    # send serialized public key
    connectSocket.sendall(public_key_b)

    # receive symmetric key and decrypt it
    serverKey_enc = connectSocket.recv(4096)
    serverKey = private_key.decrypt(
        serverKey_enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    fernet = Fernet(serverKey)
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

print("Welcome to P2Python!")
frame1 = tk.Frame(
    window,
    bg=PALETTE["bg"]
)
frame2 = tk.Frame(
    window,
    bg=PALETTE["bg"]
)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
public_key_b: bytes = public_key.public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

friendip = tk.StringVar(window)
friend = tk.Entry(
    frame1,
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    font="Consolas 14",
    width=15,
    textvariable=friendip
)

connect = tk.Button(
    frame1,
    text="Connect",
    font="Consolas 14",
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    activebackground=PALETTE["activebackground"],
    activeforeground=PALETTE["activeforeground"],
    command=lambda: connectF(friendip.get())
)

message = tk.StringVar(window)
textInput = tk.Entry(
    frame2,
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    font="Consolas 14",
    width=15,
    textvariable=message
)

sendText = tk.Button(
    frame2,
    text="Send!",
    font="Consolas 14",
    bg=PALETTE["bg"],
    fg=PALETTE["fg"],
    activebackground=PALETTE["activebackground"],
    activeforeground=PALETTE["activeforeground"],
    command=lambda: send_message(message.get())
)


friend.pack(side='left')
connect.pack(side='left')
frame1.pack()

textInput.pack(side='left')
sendText.pack(side='left')
frame2.pack()

text.pack()

window.mainloop()
