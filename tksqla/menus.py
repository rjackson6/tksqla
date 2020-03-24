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
        settings_menu.add_command(label='Preferences...', command=self.callbacks['settings--preferences'])
        self.add_cascade(label='Settings', menu=settings_menu)


class Preferences(tk.Frame):
    def __init__(self, parent, callbacks, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.settings = settings
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        left_frame = tk.Frame(self, bg='bisque')
        right_frame = tk.Frame(self, bg='lightblue')
        left_frame.grid(row=0, column=0, sticky='NSEW')
        right_frame.grid(row=0, column=1, sticky='NSEW')
        left_frame.columnconfigure(0, weight=1)
        # placeholder label
        self.pref_tree = ttk.Treeview(left_frame)
        self.pref_tree.bind('<<TreeviewSelect>>', self.treeview_select)
        self.pref_tree.insert('', 'end', iid='appearance', text='Appearance!')
        self.pref_tree.insert('', 'end', iid='general', text='General Settings!')
        self.pref_tree.grid(row=0, column=0)

        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        self.appearance_frame = PreferencesAppearance(right_frame, self.callbacks, self.settings)
        self.general_frame = PreferencesGeneral(right_frame, self.callbacks)
        self.appearance_frame.grid(row=0, column=0, sticky='NSEW')
        self.general_frame.grid(row=0, column=0, sticky='NSEW')

    def treeview_select(self, event):
        selection = self.pref_tree.selection()
        iid = selection[0]  # first value in the tuple
        if iid == 'appearance':
            self.appearance_frame.lift()
        elif iid == 'general':
            self.general_frame.lift()


class PreferencesAppearance(tk.Frame):
    def __init__(self, parent, callbacks, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.settings = settings

        self.inputs = {}
        self.font_size_var = tk.IntVar()
        self.font_size_var.set(16)
        self.font_size_label = ttk.Label(self, text='Font size')
        self.inputs['fontsize'] = tk.Spinbox(self, textvariable=self.font_size_var)
        # Layout
        self.font_size_label.grid(row=0, column=0)
        self.inputs['fontsize'].grid(row=0, column=1)

        self.apply_btn = tk.Button(self, text='Apply', command=self.test_font)
        self.apply_btn.configure(font=('Times New Roman', self.font_size_var.get()))
        self.apply_btn.grid(row=1, column=1)

    def test_font(self):
        self.font_size_var.set(48)
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        self.callbacks['settings--preferences--update'](data)


class PreferencesGeneral(tk.Frame):
    def __init__(self, parent, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = ttk.Label(self, text='Placeholder for general settings')
        self.placeholder.grid(row=0, column=0)
