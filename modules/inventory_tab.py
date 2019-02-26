# Inventory tab to keep a count on owned cards
import tkinter as tk
import os.path


ALL = "Library"
INVENTORY = "./storage/inventory.csv"
CARD = "CARD"
GROUP = "GROUP"


def print_nyan():
    print("Nyanpasu!")


def get_groups():
    groups = []
    check_inventory_file()
    inv = open(INVENTORY, "r+")
    for line in inv.readlines():
        item_type = line.split(",")[0]
        if item_type == GROUP:
            groups.append(line.split(",")[1].rstrip())
    inv.close()
    return groups


def check_inventory_file():
    if not os.path.isdir("./storage"):
        os.mkdir("./storage", 0o755)
    if not os.path.exists(INVENTORY):
        file = open(INVENTORY, "w+")
        file.close()


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
        self.manage = tk.Button(self.search_frame, text="Manage Groups", command=self.manage_groups, width=15, height=1)

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
        check_inventory_file()

    def manage_groups(self):
        manage = tk.Toplevel(self.client.window)
        manage.wm_title("Manage Groups")
        # manage.geometry("400x75")
        manage.resizable(False, False)
        manage.grab_set()

        # Requires 4 things: Entry + add, dropdown + remove
        dropdown_var = tk.StringVar(manage)
        dropdown_var.set("Select a group")
        groups = get_groups()

        def accept():
            # Check if entered text is valid
            new = entry.get()
            if new == "" or new.find(',') != -1 or new in groups:
                return
            inv = open(INVENTORY, "a")
            inv.write(GROUP + "," + entry.get() + "\n")
            inv.close()
            entry.delete(0, "end")
            groups.append(new)
            update_menu()

        def remove():
            # Check remove
            if dropdown_var.get() == "Select a group":
                return
            inv = open(INVENTORY, "r+")
            data = inv.readlines()
            inv.close()

            inv = open(INVENTORY, "w")
            for line in data:
                if line.split(',')[0] != GROUP:
                    inv.write(line)
                elif line.split(',')[1].rstrip('\r\n') != dropdown_var.get():
                    inv.write(line)
            inv.close()
            groups.remove(dropdown_var.get())
            dropdown_var.set("Select a group")
            update_menu()

        def update_menu():
            menu = dropdown["menu"]
            menu.delete(0, "end")
            for option in groups:
                menu.add_command(label=option, command=lambda value=option: dropdown_var.set(value))

        add_button = tk.Button(manage, text="Add", height=1, width=15, command=accept)
        remove_button = tk.Button(manage, text="Remove", height=1, width=15, command=remove)

        entry = tk.Entry(manage)
        dropdown = tk.OptionMenu(manage, dropdown_var, *groups)
        dropdown.config(width=40)

        manage.rowconfigure([0, 1], weight=1)
        manage.columnconfigure(0, weight=4)
        manage.columnconfigure(1, weight=1)

        entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        dropdown.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        add_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        remove_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
