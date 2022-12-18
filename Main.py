import urllib.request
import tkinter as tk

from Backend import *

acceptSocket, connectSocket = createSockets()

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
    command=lambda: connectF_t(friendip.get(), connectSocket)
)

ip.pack()
friend.pack(side="left")
connect.pack(side="left")
frame1.pack()
window.mainloop()
