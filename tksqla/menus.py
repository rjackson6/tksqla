from tkinter import ttk
import tkinter as tk


class MainMenu(tk.Menu):
    def __init__(self, parent, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label='Quit', command=self.callbacks['file--quit'])
        self.add_cascade(label='File', menu=file_menu)

        settings_menu = tk.Menu(self, tearoff=False)
        settings_menu.add_command(label='Preferences...')
        self.add_cascade(label='Settings', menu=settings_menu)
