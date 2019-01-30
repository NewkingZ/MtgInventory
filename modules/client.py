# Client module handling the gui

import tkinter as tk
from tkinter import ttk
import modules.search_tab
from PIL import Image, ImageTk
import requests
# from tkinter import font as tkfont
# import modules.mtgcards as mtg
import re


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
        self.card_frame.grid_propagate(False)
        self.card_frame.rowconfigure(0, weight=4)
        self.card_frame.rowconfigure(1, weight=3)
        self.card_frame.columnconfigure(0, weight=1)
        self.card_frame.grid_propagate(False)

        self.card_art_frame = tk.Frame(self.card_frame)
        self.card_art_frame.grid(row=0, column=0, sticky='news')
        self.card_art_frame.grid_propagate(False)
        self.card_art_frame.rowconfigure(0, weight=1)
        self.card_art_frame.columnconfigure(0, weight=1)

        self.card_art_label = tk.Label(self.card_art_frame, font=("calibri", 25))
        self.card_art_label.grid(row=0, column=0, sticky='news')

        self.text_frame = tk.Frame(self.card_frame)
        self.text_card_name = tk.StringVar()
        self.text_set_name = tk.StringVar()
        self.text_cost = tk.StringVar()
        self.text_type_name = tk.StringVar()
        self.text_text_name = tk.StringVar()
        self.text_flavor = tk.StringVar()
        self.text_stats = tk.StringVar()

        self.text_frame.grid(row=1, column=0, sticky='news', padx=20, pady=30)
        self.text_frame.grid_propagate(False)
        self.text_frame.rowconfigure([0, 1, 4], weight=1)
        self.text_frame.rowconfigure([2, 3], weight=3)
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.columnconfigure(1, weight=1)
        tk.Label(self.text_frame, textvariable=self.text_card_name, font=("arial", "16", "bold")).\
            grid(row=0, column=0, sticky='w')
        tk.Label(self.text_frame, textvariable=self.text_type_name).grid(row=1, column=0, sticky='w')
        tk.Label(self.text_frame, textvariable=self.text_text_name).grid(row=2, column=0, sticky='we', columnspan=2)
        tk.Label(self.text_frame, textvariable=self.text_flavor, font=("arial", "10", "italic"))\
            .grid(row=3, column=0, sticky='we', columnspan=2)
        tk.Label(self.text_frame, textvariable=self.text_set_name).grid(row=0, column=1, sticky='e')
        tk.Label(self.text_frame, textvariable=self.text_cost).grid(row=1, column=1, sticky='e')
        tk.Label(self.text_frame, textvariable=self.text_stats, font=("arial", "14", "bold")).\
            grid(row=4, column=1, sticky='es')

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
            self.card_art_label.config(text="", image=card_art)
            self.card_art_label.image = card_art
            # label = tk.Label(self.card_frame, image=card_art)
            # label.image = card_art

            # label.grid(row=0, column=0, sticky='news')

        except requests.exceptions.RequestException:
            # label = tk.Label(self.card_frame, text="Image not found", font=("calibri", 25))
            # label.grid(row=0, column=0, sticky='news')
            self.card_art_label.config(text="Image not found", image='')

        # Compile some info for some of the labels

        if card.power is not None:
            stats = card.power + '/' + card.toughness
        else:
            stats = ""

        if card.flavor is None:
            flavor = ""
        else:
            flavor = card.flavor

        mana = card.mana_cost
        if mana is None:
            mana = "-"

        self.text_card_name.set(card.name)
        self.text_set_name.set(card.set)
        self.text_cost.set(re.sub(r'[{}]', "", mana))
        self.text_type_name.set(card.type)
        self.text_text_name.set(card.text)
        self.text_flavor.set(flavor)
        self.text_stats.set(stats)


