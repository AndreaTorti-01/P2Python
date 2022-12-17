from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import urllib.request
import tkinter as tk
import socket
from threading import Thread

def connectF_t():
    t = Thread(target=connectF)
    t.daemon = True
    t.start()
def connectF():
    addr = friendip.get().split(":")
    port = int(addr[1])
    connectSocket.connect((addr[0], port))
    print("connected!")

def acceptF_t():
    t = Thread(target=acceptF)
    t.daemon = True
    t.start()
    print("server ready!")
def acceptF():
    _, addr = acceptSocket.accept()
    print(addr, "connected")

HOST = "0.0.0.0"
acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acceptSocket.bind((HOST, 0))
acceptSocket.listen()
acceptF_t()

palette = {
    "bg": "#4a4d4d",
    "fg": "#ffffff",
    "activebackground": "#656868",
    "activeforeground": "#ffffff"
}

external_ip = urllib.request.urlopen(
    'https://v4.ident.me/').read().decode('utf8')

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# b for bytes, each char max 8 lenght
message = b'encrypt me!'

encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

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
    command=connectF_t
)

ip.pack()
friend.pack(side="left")
connect.pack(side="left")
frame1.pack()
window.mainloop()
