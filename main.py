#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Mtg Inventory app

# import libraries here
import tkinter as tk
import modules.client as client

import msvcrt as m
import traceback

# Initialize client
try:
    root = tk.Tk()
    client.Client(root)
    root.mainloop()

except Exception as err:
    print("Error has occurred. Press Enter to continue...")
    print(err)
    traceback.print_exc()
    m.getch()
