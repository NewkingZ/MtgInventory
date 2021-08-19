# Inventory tab to keep a count on owned cards
import tkinter as tk
from tkinter.filedialog import askopenfilename
import libraries.collections as collections


def print_nyan():
    print("Nyanpasu!")


class InventoryFrame(tk.Frame):
    def __init__(self, client):
        tk.Frame.__init__(self, client.tab_frame)
        self.search_frame = tk.Frame(self)
        self.grid_propagate(False)
        self.client = client
        self.collections = []
        for option in collections.get_collections():
            self.collections.append(option)

        # Set up listbox and search methods
        self.search_frame = tk.Frame(self)
        self.group_var = tk.StringVar(self.search_frame)
        # Weird bug where the value for the option menu won't work
        # self.group_menu = tk.OptionMenu(self.search_frame, self.group_var, *self.collections)
        self.group_menu = tk.OptionMenu(self.search_frame, self.group_var, [])
        self.group_menu.config(height=1, width=20)
        self.group_var.set(collections.ALL)

        self.group_menu["menu"].delete(0, "end")
        self.group_menu["menu"].add_command(label=collections.ALL,
                                            command=lambda value=collections.ALL: self.group_var.set(value))
        for option in self.collections:
            self.group_menu["menu"].add_command(label=option, command=lambda value=option: self.group_var.set(value))

        self.fetch = tk.Button(self.search_frame, text="Fetch", command=self.display_collection, width=15, height=1)
        self.import_button = tk.Button(self.search_frame, text="Import", command=self.import_collection,
                                       width=15, height=1)
        self.manage = tk.Button(self.search_frame, text="Manage Collections", command=self.manage_collections, width=15,
                                height=1)

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
        self.import_button.grid(row=10, column=70, sticky='e', padx=10)
        self.manage.grid(row=10, column=80, sticky='e', padx=10)
        header_label.grid(row=20, column=10, columnspan=71, sticky='ws')

    def display_collection(self):
        print("Get collection info for: " + self.group_var.get())
        if self.group_var.get() == collections.ALL:
            print("Display for Library not yet supported")
            # TODO: Implement display for Library
            return

        collection = self.group_var.get()

    def manage_collections(self):
        manage = tk.Toplevel(self.client.window)
        manage.wm_title("Manage Collections")
        # manage.geometry("400x75")
        manage.resizable(False, False)
        manage.grab_set()

        # Requires 4 things: Entry + add, dropdown + remove
        dropdown_var = tk.StringVar(manage)
        default_selection = "Select a group"
        dropdown_var.set("Select a group")

        def accept():
            # Check if entered text is valid
            new = entry.get()
            if new == "" or new.find(',') != -1 or new in self.collections:
                return

            entry.delete(0, "end")
            collections.make_collection(new)
            # self.collections.append(new)
            update_menu()

        def remove():
            # Check remove
            if dropdown_var.get() == default_selection:
                return

            collections.remove_collection(dropdown_var.get())
            self.collections.remove(dropdown_var.get())
            dropdown_var.set("Select a group")
            update_menu()

        def update_menu():
            main_menu = self.group_menu["menu"]
            main_menu.delete(0, "end")
            menu.delete(0, "end")
            main_menu.add_command(label=collections.ALL, command=self.group_var.set(collections.ALL))
            self.collections = collections.get_collections()
            for option in self.collections:
                menu.add_command(label=option, command=lambda value=option: dropdown_var.set(value))
                main_menu.add_command(label=option, command=lambda value=option: self.group_var.set(value))

        add_button = tk.Button(manage, text="Add", height=1, width=15, command=accept)
        remove_button = tk.Button(manage, text="Remove", height=1, width=15, command=remove)

        entry = tk.Entry(manage)
        # Weird error occurs here as well
        # dropdown = tk.OptionMenu(manage, dropdown_var, *self.collections)
        dropdown = tk.OptionMenu(manage, dropdown_var, [])
        menu = dropdown["menu"]
        menu.delete(0, "end")
        for group in self.collections:
            self.group_menu["menu"].add_command(label=group, command=lambda value=group: dropdown_var.set(value))
        dropdown.config(width=40)

        manage.rowconfigure([0, 1], weight=1)
        manage.columnconfigure(0, weight=4)
        manage.columnconfigure(1, weight=1)

        entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        dropdown.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        add_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        remove_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        update_menu()

    def import_collection(self):
        import_collection = tk.Toplevel(self.client.window)
        import_collection.wm_title("Import collection")
        # import_collection.geometry("400x75")
        import_collection.resizable(False, False)
        import_collection.grab_set()

        # Requires 5 things: widgets + File search, dropdown + label, confirm
        dropdown_var = tk.StringVar(import_collection)
        default_selection = "Select collection"
        dropdown_var.set(default_selection)

        def confirm():
            # Check whether file is csv first
            import_file = collection_entry.get()
            if import_file[-4:] != ".csv" and import_file[-4:] != ".CSV":
                print("Invalid import type")
                warn_label.config(text="Invalid file type", fg="red")
                warn_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                return

            # Make sure a collection was selected
            collection_selected = dropdown_var.get()
            if collection_selected == default_selection:
                warn_label.config(text="Invalid collection", fg="red")
                warn_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                return

            # Attempt importing file into collection
            warn_label.config(text="Starting import, this can take a while", fg="orange")
            warn_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
            self.update_idletasks()
            if collections.import_card_list(import_file, collection_selected):
                warn_label.config(text="Completed Import!", fg="green")
            else:
                warn_label.config(text="A problem occurred during import", fg="red")

        def search_files():
            # Check through files
            print("Lookin for files")
            filename = askopenfilename()
            collection_entry.delete(0, "end")
            collection_entry.insert(0, filename)

        search_button = tk.Button(import_collection, text="Select file", height=1, width=10, command=search_files)
        select_collection = tk.Label(import_collection, text="Import into", height=1, width=15)
        confirm_button = tk.Button(import_collection, text="Confirm", height=1, width=10, command=confirm)
        collection_entry = tk.Entry(import_collection)
        warn_label = tk.Label(import_collection, text="", height=1, width=15)

        # Weird error occurs here as well
        # dropdown = tk.OptionMenu(manage, dropdown_var, *self.collections)
        dropdown = tk.OptionMenu(import_collection, dropdown_var, [])
        menu = dropdown["menu"]
        menu.delete(0, "end")
        for option in collections.get_collections():
            menu.add_command(label=option, command=lambda value=option: dropdown_var.set(value))
        dropdown.config(width=40)

        import_collection.rowconfigure([0, 1], weight=1)
        import_collection.columnconfigure(0, weight=4)
        import_collection.columnconfigure(1, weight=1)

        collection_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        dropdown.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        search_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        select_collection.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        confirm_button.grid(row=3, column=1, sticky="e", padx=5, pady=5)
