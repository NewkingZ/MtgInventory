# Client module handling the gui

import tkinter as tk


class Client:
    def __init__(self, root):
        self.window = root
        self.window.title("Mtg Inventory App")
        # w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        # root.geometry("%dx%d+0+0" % (w, h))
        self.window.state('zoomed')
        # Set the icon later 

