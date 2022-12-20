import tkinter as tk
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from threading import Thread
import socket
import sys
from portforwardlib import forwardPort
import urllib.request

HOST = "0.0.0.0"
PORT = 21763
CHUNK_SIZE = 64
PALETTE = {
    "bg": "#4a4d4d",
    "fg": "#ffffff",
    "activebackground": "#656868",
    "activeforeground": "#ffffff"
}


def data_chunkize_crypt_send(data: bytes, key: rsa.RSAPublicKey, sock_v: socket.socket):
    # Divide the message into chunks
    # Change this value to the desired chunk size
    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]

    # Encrypt each chunk
    encrypted_chunks = []
    for chunk in chunks:
        encrypted_chunks.append(
            key.encrypt(
                chunk,
                padding.PKCS1v15()
            )
        )

    # Concatenate the encrypted chunks
    encrypted_message = b''.join(encrypted_chunks)
    # and SEND
    sock_v.sendall(f"{len(chunks)}:".encode() + encrypted_message)


def receive_decrypt_reassemble_output(key: rsa.RSAPrivateKey, sock_v: socket.socket) -> bytes:
    data = b''
    while True:
        # Attempt to receive 4096 bytes of data
        data_p = sock_v.recv(4096)
        # If the received data is empty, there is nothing left to receive
        if not data_p:
            break
        # Add the received data to the buffer
        data += data_p
    num_chunks = int(data[:data.index(b':')].decode())
    data = data[data.index(b':'):]

    # Divide the encrypted message into chunks
    encrypted_chunks = [data[i:i + CHUNK_SIZE]
                        for i in range(num_chunks * CHUNK_SIZE, len(data), CHUNK_SIZE)]

    # Decrypt each chunk
    decrypted_chunks = []
    for chunk in encrypted_chunks:
        decrypted_chunks.append(
            key.decrypt(
                chunk,
                padding.PKCS1v15()
            )
        )

    # Concatenate the decrypted chunks
    return (b''.join(decrypted_chunks))


def acceptF_t():
    connectSocket, addr = mySocket.accept()
    print(addr, "connected")
    otherPublic_b: bytes = connectSocket.recv(4096)
    otherPublic: rsa.RSAPublicKey = serialization.load_pem_public_key(
        otherPublic_b)  # type:ignore

    data_chunkize_crypt_send(public_key_b, otherPublic, connectSocket)

    print("keys exchanged!")
    print(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo),
          otherPublic.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
public_key_b: bytes = public_key.public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
otherPublic = rsa.RSAPublicKey

UPnPt = forwardPort(PORT, PORT, None, None, False,
                    'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports opened successfully')

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((HOST, PORT))
mySocket.listen()
connectSocket = socket.socket
t = Thread(target=lambda: acceptF_t())
t.daemon = True
t.start()
print("server ready!")

external_ip = urllib.request.urlopen(
    'https://v4.ident.me/').read().decode('utf8')

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
    text=f"Your Socket-> {external_ip}:{mySocket.getsockname()[1]}"
)

ip.pack()

window.mainloop()

UPnPt = forwardPort(PORT, PORT, None, None, True,
                    'TCP', 0, 'P2Python UPnP', False)
if UPnPt == False:
    print('TCP port forwarding failed')
print('ports closed successfully')
