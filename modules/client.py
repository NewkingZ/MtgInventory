# Client module handling the gui

import tkinter as tk
from tkinter import ttk
import modules.search_tab
from PIL import Image, ImageTk
import requests
# from tkinter import font as tkfont
# import modules.mtgcards as mtg
# import re


def print_crap():
    print('crap')


class Client:
    def __init__(self, root):
        self.window = root
        self.window.title("Mtg Inventory App")
        # w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        # root.geometry("%dx%d+0+0" % (w, h))
        self.window.minsize(1000, 700)
        self.window.state('zoomed')
        # Set the icon later

        # Set up main frame elements and grid formatting
        self.window.rowconfigure([0, 99], weight=1)
        self.window.rowconfigure(1, weight=8)
        self.window.columnconfigure(0, weight=2)
        self.window.columnconfigure(99, weight=1)

        # menu_bar
        # Card View Frame
        self.card_frame = tk.Frame(self.window)
        self.card_frame.rowconfigure(1, weight=4)
        self.card_frame.rowconfigure(0, weight=2)
        self.card_frame.columnconfigure(0, weight=1)

        # text_frame = tk.Frame(self.card_frame)
        # text_frame.grid(row=0, column=0, sticky='news')

        # Separator
        ttk.Separator(self.window, orient=tk.VERTICAL).grid(column=1, row=1, sticky='ns')
        # Tab Frame
        self.tab_frame = ttk.Notebook(self.window)
        search_frame = modules.search_tab.SearchFrame(self)
        inventory_frame = tk.Frame(self.tab_frame)
        deck_frame = tk.Frame(self.tab_frame)
        self.tab_frame.add(search_frame, text="Search")
        self.tab_frame.add(inventory_frame, text="Inventory")
        self.tab_frame.add(deck_frame, text="Decks")
        self.tab_frame.grid_propagate(False)

        self.tab_frame.grid(row=0, column=0, rowspan=100, sticky='news', padx=20, pady=30)
        self.card_frame.grid(row=0, column=99, rowspan=100, sticky='news', padx=20, pady=30)

    def update_display(self, card):
        url = card.image_url
        try:
            resp = requests.get(url, stream=True).raw
            img = Image.open(resp)
            img = img.resize((300, 418), Image.ANTIALIAS)
            card_art = ImageTk.PhotoImage(img)
            label = tk.Label(self.card_frame, image=card_art, bg="blue")
            label.image = card_art

            label.grid(row=0, column=0, sticky='news')

        except requests.exceptions.RequestException:
            label = tk.Label(self.card_frame, text="Image not found")
            label.grid(row=0, column=0, sticky='news')




