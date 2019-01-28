# Search tab to find cards for decks and inventory
import tkinter as tk
# from tkinter import ttk
# from tkinter import font as tkfont
import modules.mtgcards as mtg
import re


class SearchFrame(tk.Frame):
    def __init__(self, client):
        tk.Frame.__init__(self, client.tab_frame)

        # 2 main elements, search frame with options and the listbox
        self.search_frame = tk.Frame(self)
        self.client = client
        self.list = tk.Listbox(self, font='TkFixedFont')
        self.filter = tk.Frame(self)

        self.columnconfigure(10, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(5, weight=5)
        self.rowconfigure(10, weight=15)
        self.rowconfigure(99, weight=0)

        self.search_frame.grid(row=0, column=10, sticky='news')
        self.filter.grid(row=5, column=10, sticky='news')
        self.list.grid(row=10, column=10, sticky='news')

        # Search frame stuff settings
        self.search_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.search_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)

        self.search_name = tk.Entry(self.search_frame)
        # self.search.insert(tk.END, "Card Name")
        self.search_button = tk.Button(self.search_frame, text="search", command=self.search_mtg, width=15)

        self.search_name.grid(row=0, columnspan=5, column=0, sticky='new', padx=10, pady=10)
        self.search_button.grid(row=0, column=99, sticky="ne", padx=10, pady=10)
        self.results = []
        self.currently_shown = None

        def on_select(evt):
            lb = evt.widget
            self.client.update_display(self.results[int(lb.curselection()[0])])

        self.list.bind('<<ListboxSelect>>', on_select)

    def search_mtg(self):
        name = self.search_name.get()
        if name is "":
            return
        cards = mtg.fetch(name)
        self.list.delete(first=0, last=tk.END)
        for card in cards:
            self.card_found(card)
        self.results = cards

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
