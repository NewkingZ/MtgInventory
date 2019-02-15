# Search tab to find cards for decks and inventory
import tkinter as tk
# from tkinter import ttk
# from tkinter import font as tkfont
import modules.mtgcards as mtg
import re


class SearchFrame(tk.Frame):
    def __init__(self, client):
        tk.Frame.__init__(self, client.tab_frame)
        self.grid_propagate(False)
        # 3 main elements:
        #  Search frame with entry and search button
        #  Filter frame with filter options + headers
        #  Listbox with search results
        self.search_frame = tk.Frame(self)
        self.client = client
        self.filter = tk.Frame(self)
        self.list = tk.Listbox(self, font='TkFixedFont')
        scrollbar = tk.Scrollbar(self.list, orient="vertical")
        self.list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list.yview)
        header_titles = "Name" + (" "*46) + "Set" + " "*42 + "Rarity" + "  " + "Mana cost"
        list_header = tk.Label(self.filter, text=header_titles, font='TkFixedFont')

        # Grid settings for the whole search tab
        self.columnconfigure(10, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(5, weight=3)
        self.rowconfigure(10, weight=15)
        self.rowconfigure(99, weight=0)

        # Grid settings for the search frame (Entry, search button)
        self.search_frame.grid(row=0, column=10, sticky='news')
        self.search_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.search_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)

        # Filter Frame
        self.filter.rowconfigure([5, 10], weight=1)
        self.filter.columnconfigure(10, weight=1)
        self.filter.grid(row=5, column=10, sticky='news')
        tk.Label(self.filter, text="This section is dedicated to filter options which will be implemented later",
                 font=("Arial", "10", "bold")).grid(row=5, column=10, sticky='news')

        list_header.grid(row=10, column=10, sticky='ws')

        # Grid settings for the listbox
        self.list.columnconfigure(0, weight=1)
        self.list.rowconfigure(0, weight=1)
        self.list.grid(row=10, column=10, sticky='news')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.search_name = tk.Entry(self.search_frame)
        # self.search.insert(tk.END, "Card Name")
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_mtg, width=15)

        self.search_name.grid(row=0, columnspan=5, column=0, sticky='new', padx=10, pady=10)
        self.search_button.grid(row=0, column=99, sticky="ne", padx=10, pady=10)
        self.results = []
        self.currently_shown = None

        def on_list_select(evt):
            # Index Error occurs when double clicking the Search Entry field after having selected a card
            try:
                self.client.update_display(self.results[int(self.list.curselection()[0])])
            except IndexError:
                pass

        def on_search_select(evt):
            self.search_name.select_range(0, tk.END)

        self.list.bind('<<ListboxSelect>>', on_list_select)
        self.search_name.bind('<FocusIn>', on_search_select)

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
                    [card.rarity[0], 8],
                    [re.sub(r'[{}]', "", mana), 0]]

        card_data = ""
        for item in elements:
            try:
                card_data += item[0] + " " * (item[1] - len(item[0]))

            except TypeError:
                card_data += "-" + " " * (50 - len("-"))

        self.list.insert(tk.END, card_data)

    def enter_pressed(self, evt):
        # When the enter button is pressed, this command will run.
        # Confirm the text box is selected before searching for the cards
        print(evt.widget)
        if evt.widget is self.search_name:
            self.search_mtg()
