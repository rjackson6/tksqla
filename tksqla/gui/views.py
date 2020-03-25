from tkinter import ttk
import tkinter as tk
from . import widgets as w


class VehicleTrimView(tk.Frame):
    def __init__(self, parent, data, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.data = data
        self.treeview = ttk.Treeview(self, columns=('Make', 'Model', 'Trim'))
        self.treeview.heading('Make', text='Make')
        self.treeview.heading('Model', text='Model')
        self.treeview.heading('Trim', text='Trim')
        # Layout
        self.treeview.grid(row=0, column=0)
        self.load_records()

    def load_records(self):
        for key, record in self.data.items():
            self.treeview.insert('', 'end', iid=key, text='Trim ID: {}'.format(key),
                                 values=[record['make'], record['model'], record['trim']])
