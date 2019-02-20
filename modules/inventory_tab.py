# Inventory tab to keep a count on owned cards
import tkinter as tk


ALL = "Library"


def print_nyan():
    print("Nyanpasu!")


class InventoryFrame(tk.Frame):
    def __init__(self, client):
        tk.Frame.__init__(self, client.tab_frame)
        self.search_frame = tk.Frame(self)
        self.grid_propagate(False)
        self.client = client

        # Set up listbox and search methods
        self.search_frame = tk.Frame(self)
        self.group_var = tk.StringVar(self.search_frame)
        self.group_menu = tk.OptionMenu(self.search_frame, self.group_var, ALL)
        self.group_menu.config(height=1, width=20)
        self.group_var.set(ALL)

        self.fetch = tk.Button(self.search_frame, text="Fetch", command=print_nyan, width=15, height=1)
        self.manage = tk.Button(self.search_frame, text="Manage Groups", command=print_nyan, width=15, height=1)

        self.list = tk.Listbox(self, font='TkFixedFont')
        scrollbar = tk.Scrollbar(self.list, orient="vertical")
        self.list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list.yview)

        # Maybe remove set from headers for set code instead

        # Place name, set code, cost, rarity, group location
        header_titles = "Name" + " " * 46 + "Set" + " " * 6 + "Rarity" + "    " + "Mana cost" + " " * 8 + "Location"
        header_label = tk.Label(self.search_frame, text=header_titles, font='TkFixedFont')

        # Configure columns and rows for main frame:
        self.rowconfigure(50, weight=99)
        self.rowconfigure(10, weight=1)
        self.columnconfigure(10, weight=1)

        # Place main elements
        self.search_frame.grid(row=10, column=10, sticky='news', pady=(10, 0))
        self.list.grid(row=50, column=10, columnspan=71, sticky='news')
        self.list.columnconfigure(0, weight=1)
        self.list.rowconfigure(0, weight=1)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure columns and rows for search frame:
        self.search_frame.rowconfigure([10, 20], weight=1)
        self.search_frame.columnconfigure([10, 20, 30, 40, 50, 60, 70, 80], weight=1)
        # self.search_frame.grid_propagate(False)

        # Place Search frame elements
        self.group_menu.grid(row=10, column=10, sticky='we', padx=15)
        self.fetch.grid(row=10, column=20, sticky='w')
        self.manage.grid(row=10, column=80, sticky='e', padx=10)
        header_label.grid(row=20, column=10, columnspan=71, sticky='ws')

        # Excel initialize
