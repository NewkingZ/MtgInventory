#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Mtg Inventory app

# import libraries here
import tkinter as tk
import modules.client as client

# Initialize client
root = tk.Tk()
client.Client(root)
root.mainloop()
