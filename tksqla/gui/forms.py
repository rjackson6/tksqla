from tkinter import ttk
import tkinter as tk
from . import widgets as w


class VehicleMakeForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.fields = {}
        self.fields['name'] = w.FormField(self, fields['name'], widget_cls=w.CharEntry)
        self.save_btn = ttk.Button(self, text='Save', command=self.callbacks['on_save_vehiclemake_form'])
        # Layout
        self.fields['name'].grid(column=0, row=1)
        self.save_btn.grid(column=0, row=2)

    def is_valid(self):
        valid = True
        for key, widget in self.fields.items():
            if not widget.is_valid():
                valid = False
        return valid

    def get(self):
        data = {'name': self.fields['name'].get()}
        return data


class VehicleModelForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.fields = {}
        # Inputs
        self.vehiclemake_lookups = fields['vehiclemake']['values']
        self.fields['vehiclemake'] = w.FormField(self, fields['vehiclemake'], w.Combobox,
                                                 input_kwargs={'lookups': self.vehiclemake_lookups})
        if fields['vehiclemake']['disabled']:
            self.fields['vehiclemake'].input.state(['disabled'])
        if 'initial' in fields['vehiclemake']:
            self.fields['vehiclemake'].input.set(fields['vehiclemake']['initial'])
        self.name_var = tk.StringVar()
        self.fields['name'] = w.FormField(self, fields['name'], w.CharEntry,
                                          input_kwargs={'textvariable': self.name_var})
        self.save_btn = ttk.Button(self, text='Save', command=self.callbacks['on_save_vehiclemodel_form'])
        # Layout
        self.fields['vehiclemake'].grid(column=0, row=1)
        self.fields['name'].grid(column=1, row=1)
        self.save_btn.grid(column=1, row=2)

    def get(self):
        vehiclemake = self.fields['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        name = self.fields['name'].get()
        data = {'vehiclemake_id': vehiclemake_id, 'name': name}
        return data


class VehicleTrimForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.fields = {}
        # Lookups and inputs
        self.vehiclemake_lookups = fields['vehiclemake']['values']
        self.fields['vehiclemake'] = w.FormField(self, fields['vehiclemake'], w.Combobox,
                                                 input_kwargs={'lookups': self.vehiclemake_lookups})
        self.vehiclemodel_lookups = fields['vehiclemodel']['values']
        self.fields['vehiclemodel'] = w.FormField(self, fields['vehiclemodel'], w.Combobox,
                                                  input_kwargs={'lookups': self.vehiclemodel_lookups})
        self.vehicletrim_name_var = tk.StringVar()
        self.fields['name'] = w.FormField(self, fields['name'], w.CharEntry,
                                          input_kwargs={'textvariable': self.vehicletrim_name_var})
        # Bindings
        self.fields['vehiclemake'].input.bind('<<ComboboxSelected>>', self.on_vehiclemake_selected)
        self.fields['vehiclemodel'].input.bind('<<ComboboxSelected>>', self.on_vehiclemodel_selected)
        # Buttons to open new forms
        self.vehiclemake_form_btn = ttk.Button(
            self, text='Add VehicleMake',
            command=lambda: self.callbacks['open_vehiclemake_form'](called_from=self, modal=True)
        )
        self.vehiclemodel_form_btn = ttk.Button(
            self, text='Add VehicleModel',
            command=lambda: self.callbacks['open_vehiclemodel_form'](called_from=self, modal=True)
        )
        # A save button
        self.save_btn = ttk.Button(self, text='Save',
                                   command=self.callbacks['on_save_vehicletrim_form'])
        # Default states
        self.fields['vehiclemodel'].input.state(['disabled'])
        self.vehiclemodel_form_btn.state(['disabled'])
        self.fields['name'].input.state(['disabled'])
        # Layout
        self.fields['vehiclemake'].grid(column=0, row=1)
        self.fields['vehiclemodel'].grid(column=1, row=1)
        self.fields['name'].grid(column=2, row=1)
        self.vehiclemake_form_btn.grid(column=0, row=2)
        self.vehiclemodel_form_btn.grid(column=1, row=2)
        self.save_btn.grid(column=2, row=3)

    def get(self):
        vehiclemodel = self.fields['vehiclemodel'].get()
        vehiclemodel_id = self.vehiclemodel_lookups[vehiclemodel]
        name = self.fields['name'].get()
        data = {'vehiclemodel_id': vehiclemodel_id, 'name': name}
        return data

    def reset(self):
        self.fields['vehiclemake'].input.set('')
        self.fields['vehiclemodel'].input.set('')
        self.vehicletrim_name_var.set('')

    def get_vehiclemake_id(self):
        vehiclemake = self.fields['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        return vehiclemake_id

    def on_vehiclemake_saved(self, new_record):
        self.vehiclemake_lookups = self.callbacks['qry_vehiclemake']()
        new_values = ['', *sorted(self.vehiclemake_lookups)]
        idx = new_values.index(new_record['name'])
        self.fields['vehiclemake'].input.configure(values=new_values)
        self.fields['vehiclemake'].input.current(idx)
        self.fields['vehiclemake'].input.event_generate('<<ComboboxSelected>>')

    def on_vehiclemodel_saved(self, new_record):
        vehiclemake = self.fields['vehiclemake'].get()
        vehiclemake_id = self.vehiclemake_lookups[vehiclemake]
        self.vehiclemodel_lookups = self.callbacks['filter_vehiclemodel_by_vehiclemake'](vehiclemake_id)
        new_values = ['', *sorted(self.vehiclemodel_lookups)]
        idx = new_values.index(new_record['name'])
        self.fields['vehiclemodel'].input.configure(values=new_values)
        self.fields['vehiclemodel'].input.current(idx)
        self.fields['vehiclemodel'].input.event_generate('<<ComboboxSelected>>')

    def on_vehiclemake_selected(self, event):
        selected_value = self.fields['vehiclemake'].get()
        if selected_value == '':
            self.fields['vehiclemodel'].input.state(['disabled'])
            self.vehiclemodel_form_btn.state(['disabled'])
            self.fields['name'].input.state(['disabled'])
        else:
            vehiclemake_id = self.vehiclemake_lookups.get(selected_value)
            if vehiclemake_id is None:
                return  # testing combobox
            self.vehiclemodel_lookups = self.callbacks['filter_vehiclemodel_by_vehiclemake'](vehiclemake_id)
            self.fields['vehiclemodel'].input.configure(values=['', *sorted(self.vehiclemodel_lookups)])
            self.fields['vehiclemodel'].input.state(['!disabled'])
            self.vehiclemodel_form_btn.state(['!disabled'])
            self.fields['name'].input.state(['disabled'])
        self.fields['vehiclemodel'].input.set('')
        self.vehicletrim_name_var.set('')

    def on_vehiclemodel_selected(self, event):
        selected_value = self.fields['vehiclemodel'].get()
        if selected_value == '':
            self.fields['name'].input.state(['disabled'])
        else:
            self.fields['name'].input.state(['!disabled'])
