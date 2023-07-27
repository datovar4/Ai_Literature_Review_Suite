#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 08:49:48 2023

@author: David Tovar
"""

import tkinter as tk
from tkinter import messagebox
import os

def check_api_key(filename, api_name):
    def save_api_key():
        api_key = api_key_entry.get()
        with open(filename, "w") as f:
            f.write(api_key)
        messagebox.showinfo("Saved", f"{api_name} API Key has been saved to {filename}")
        api_key_window.quit()

    if not os.path.exists(filename):
        api_key_window = tk.Tk()
        api_key_window.title(f"Enter {api_name} API Key")

        api_key_label = tk.Label(api_key_window, text=f"Please enter your {api_name} API Key:")
        api_key_label.pack()

        api_key_entry = tk.Entry(api_key_window)
        api_key_entry.pack()

        api_key_button = tk.Button(api_key_window, text="Save", command=save_api_key)
        api_key_button.pack()

        api_key_window.mainloop()
        del api_key_window
