from tkinter import font as tkfont
from tkinter import ttk
from .constants import DEFAULT_CONFIG
from .ext.themes import THEMES
import configparser


class AppConfig:
    def __init__(self):
        self.cp = configparser.ConfigParser()
        self._load_themes()
        self.load()

    def _load_themes(self):
        style = ttk.Style()
        for k, v in THEMES.items():
            style.theme_create(k, v['parent'], v['settings'])
        # style.theme_use('Dark')
        print(style.theme_names())

    def _update_font(self):
        for font in ('TkHeadingFont', 'TkTextFont', 'TkDefaultFont'):
            f = tkfont.nametofont(font)
            f.configure(size=self.cp['Appearance']['fontsize'])
        return

    def save(self):
        with open('settings.ini', 'w') as configfile:
            self.cp.write(configfile)
        return

    def load(self):
        self.cp.read_dict(DEFAULT_CONFIG)
        self.cp.read('settings.ini')
        self._update_font()
        return

    def update_settings(self, data):
        if 'fontsize' in data:
            self.cp.set('Appearance', 'fontsize', data['fontsize'])
            self._update_font()
        self.save()
        return
