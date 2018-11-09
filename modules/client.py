# Client module handling the gui

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import modules.mtgcards as mtg
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
        # Separator
        ttk.Separator(self.window, orient=tk.VERTICAL).grid(column=1, row=1, sticky='ns')
        # Tab Frame
        tab_frame = ttk.Notebook(self.window)
        search_frame = SearchFrame(tab_frame)
        inventory_frame = tk.Frame(tab_frame)
        deck_frame = tk.Frame(tab_frame)
        tab_frame.add(search_frame, text="Search")
        tab_frame.add(inventory_frame, text="Inventory")
        tab_frame.add(deck_frame, text="Decks")
        tab_frame.grid_propagate(False)

        tab_frame.grid(row=0, column=0, rowspan=100, sticky='news', padx=20, pady=30)


class SearchFrame(tk.Frame):
    def __init__(self, tabs_frame):
        tk.Frame.__init__(self, tabs_frame)

        # 2 main elements, search frame with options and the listbox
        self.search_frame = tk.Frame(self)
        self.list = tk.Listbox(self, font='TkFixedFont')

        self.columnconfigure(10, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(10, weight=15)
        self.rowconfigure(99, weight=0)

        self.search_frame.grid(row=0, column=10, sticky='news')
        self.list.grid(row=10, column=10, sticky='news')

        # Search frame stuff settings
        self.search_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.search_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)

        self.search_name = tk.Entry(self.search_frame)
        # self.search.insert(tk.END, "Card Name")
        self.search_button = tk.Button(self.search_frame, text="search", command=self.search_mtg, width=15)

        self.search_name.grid(row=0, columnspan=5, column=0, sticky='new', padx=10, pady=10)
        self.search_button.grid(row=0, column=99, sticky="ne", padx=10, pady=10)

    def search_mtg(self):
        name = self.search_name.get()
        if name is "":
            return
        cards = mtg.fetch(name)
        self.list.delete(first=0, last=tk.END)
        for card in cards:
            self.card_found(card)

    def card_found(self, card):
        # Sort elements by their properties and spacing
        mana = card.mana_cost
        if mana is None:
            mana = "-"

        elements = [[card.name, 50],
                    [card.set_name, 45],
                    [card.rarity[0], 5],
                    [re.sub(r'[{}]', "", mana), 0]]

        card_data = ""
        for item in elements:
            try:
                card_data += item[0] + " " * (item[1] - len(item[0]))

            except TypeError:
                card_data += "-" + " " * (50 - len("-"))

        self.list.insert(tk.END, card_data)



