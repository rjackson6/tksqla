from tkinter import font as tkfont
from .constants import DEFAULT_CONFIG
import configparser


class AppConfig:
    def __init__(self):
        self.cp = configparser.ConfigParser()
        self.load()

    def save(self):
        with open('settings.ini', 'w') as configfile:
            self.cp.write(configfile)
        return

    def load(self):
        self.cp.read_dict(DEFAULT_CONFIG)
        self.cp.read('settings.ini')
        for font in ('TkHeadingFont', 'TkTextFont', 'TkDefaultFont'):
            f = tkfont.nametofont(font)
            f.configure(size=self.cp['Appearance']['fontsize'])
        return

    def update_settings(self, data):
        # needs whatever values that have been updated
        self.save()

"""
        s = ttk.Style()
        self.load_settings()
        print(tkfont.names())
"""