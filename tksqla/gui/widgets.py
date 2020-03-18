from tkinter import ttk
import tkinter as tk


class Toplevel(tk.Toplevel):
    def __init__(self, parent, called_from=None, modal=False, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.called_from = called_from
        self.modal = modal


class CharEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        vcmd = self.register(self._validate_all)
        invcmd = self.register(self._invalid_command)
        self.tk_var = kwargs.get('textvariable') or tk.StringVar()
        self.configure(
            validate='all',
            validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V'),
            invalidcommand=(invcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V')
        )

    def _validate_all(self, d, i, P, s, S, v, V):
        if V == 'focusout':
            self._validate_focusout(s)
        return True

    def _validate_focusout(self, s):
        s = s.strip()
        self.tk_var.set(s)

    def _invalid_command(self, d, i, P, s, S, v, V):
        print('Invalid! d:{} i:{} P:{} s:{} S:{} v:{} V:{}'.format(d, i, P, s, S, v, V))


class Combobox(ttk.Combobox):
    def __init__(self, parent, lookups=None, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.lookups = lookups or {}
        vcmd = self.register(self._validate_all)
        invcmd = self.register(self._invalid_command)
        self.configure(
            validate='all',
            validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V'),
            invalidcommand=(invcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V'),
            values=['', *sorted(self.lookups)]
        )

    def _validate_all(self, d, i, P, s, S, v, V):
        print('d:{} i:{} P:{} s:{} S:{} v:{} V:{}'.format(d, i, P, s, S, v, V))
        if V == 'focusout':
            self._validate_focusout(s)
        elif V == 'key':
            self._validate_key(d, i, P, s, S)
        return True

    def _validate_key(self, d, i, P, s, S):
        if P and d == '1':
            for key in self.lookups:
                if key.casefold().startswith(P.casefold()):
                    autocomplete = key
                    n = len(S)
                    new_index = int(i) + n
                    self.set(autocomplete)
                    self.select_range(new_index, tk.END)
                    self.icursor(new_index)
                    break

    def _validate_focusout(self, s):
        s = s.strip()
        return True

    def _invalid_command(self, d, i, P, s, S, v, V):
        print('Invalid! d:{} i:{} P:{} s:{} S:{} v:{} V:{}'.format(d, i, P, s, S, v, V))


class FormField(ttk.Frame):
    def __init__(self, parent, field_cfg, widget_cls, input_kwargs=None, *args, **kwargs):
        super().__init__(parent, **kwargs)
        input_kwargs = input_kwargs or {}
        self.required = field_cfg['required']
        self.lookups = input_kwargs.get('lookups')
        # Variables
        self.input_var = input_kwargs.get('textvariable')
        if not self.input_var:
            if widget_cls in (CharEntry, Combobox):
                self.input_var = tk.StringVar()
            else:
                self.input_var = tk.StringVar()  # Default
        # Widgets
        if widget_cls == Combobox:
            self.input = widget_cls(self, lookups=self.lookups)
        else:
            self.input = widget_cls(self)
        self.input.configure(textvariable=self.input_var)

        # Label and Errors
        self.label = ttk.Label(self, text=field_cfg['label'])
        self.error_var = tk.StringVar()
        self.errors = ttk.Label(self, textvariable=self.error_var)
        # Layout
        self.label.grid(row=0, column=0)
        self.input.grid(row=1, column=0)
        self.errors.grid(row=2, column=0)

    def is_valid(self):
        self.input.validate()
        current_value = self.input_var.get()
        if self.required:
            if not current_value:
                self.error_var.set('This field is required')
                return False
        return True

    def get(self):
        if self.input_var:
            return self.input_var.get()
