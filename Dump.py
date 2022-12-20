import sys

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text, (self.tag,))
        self.widget.configure(state="disabled")

import tkinter as tk

# Create a Tkinter window and a Text widget
root = tk.Tk()
text = tk.Text(root)

# Redirect print output to the Text widget
sys.stdout = TextRedirector(text, "stdout")

text.pack()



root.mainloop()