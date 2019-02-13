# Inventory tab to keep a count on owned cards
import tkinter as tk


ALL = "Library"


def print_nyan():
    print("Nyanpasu!")


class InventoryFrame(tk.Frame):
    def __init__(self, client):
        tk.Frame.__init__(self, client.tab_frame)
        self.search_frame = tk.Frame(self)
        self.client = client

        # Set up listbox and search methods
        group_label = tk.Label(self, text="Group")
        self.group_var = tk.StringVar(self)
        self.group_menu = tk.OptionMenu(self, self.group_var, "Select group to search")
        self.group_menu.config(height=1, width=20)
        self.group_var.set(ALL)

        self.fetch = tk.Button(self, text="Fetch", command=print_nyan, width=15, height=1)
        self.manage = tk.Button(self, text="Manage Groups", command=print_nyan, width=15, height=1)

        self.list = tk.Listbox(self, font='TkFixedFont')
        scrollbar = tk.Scrollbar(self.list, orient="vertical")
        self.list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list.yview)

        # Maybe remove set from headers for set code instead
        header_titles = "Name" + (" " * 46) + "Set" + " " * 42 + "Rarity" + "  " + "Mana cost"
        header_label = tk.Label(self, text=header_titles, font='TkFixedFont')

        # Configure columns and rows:
        self.rowconfigure(50, weight=118)
        self.rowconfigure([11, 12], weight=1)
        self.columnconfigure([10, 20, 30, 40, 50, 60, 70, 80], weight=1)

        self.list.columnconfigure(0, weight=1)
        self.list.rowconfigure(0, weight=1)
        scrollbar.grid(row=0, column=1, sticky='ns')
        group_label.grid(row=10, column=10, sticky='we')
        self.group_menu.grid(row=11, column=10, sticky='we', padx=15)
        self.fetch.grid(row=11, column=20, sticky='w')
        self.manage.grid(row=11, column=80, sticky='e', padx=10)
        header_label.grid(row=12, column=10, columnspan=41, sticky='w')
        self.list.grid(row=50, column=10, columnspan=71, sticky='news')


