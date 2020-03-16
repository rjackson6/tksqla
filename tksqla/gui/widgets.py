from tkinter import ttk
import tkinter as tk


class Toplevel(tk.Toplevel):
    def __init__(self, parent, called_from=None, modal=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.called_from = called_from
        self.modal = modal


class CharEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
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
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)


class FormField(tk.Frame):
    def __init__(self, parent, label_text, widget_cls, required=True, field_args=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.required = required
        self.lookups = field_args
        print(self.lookups)
        # needs label, input widget class, variable+label for errors
        # Variables
        if widget_cls == ttk.Entry:
            self.field_var = tk.StringVar()
        else:
            self.field_var = None  # Placeholder
        self.error_var = tk.StringVar()
        # Widgets
        self.label = ttk.Label(self, text=label_text)
        self.field = widget_cls(self, textvariable=self.field_var)
        self.errors = ttk.Label(self, textvariable=self.error_var)
        # Layout
        self.label.grid(row=0, column=0)
        self.field.grid(row=1, column=0)
        self.errors.grid(row=2, column=0)

    def is_valid(self):
        self.field.validate()
        current_value = self.field_var.get()
        if self.required:
            if not current_value:
                self.error_var.set('This field is required')
                return False
        return True

    def get(self):
        return self.field_var.get()

# class RequiredEntry(ttk.Entry):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         vcmd = self.register(self.useless)
#         self.configure(
#             validate='all',
#             validatecommand=(vcmd, '%v', '%V')
#         )
#         self.state(['invalid'])
#         print(self.state())
#
#     def _focusout_validate(self, subcode_v, subcode_V):
#         print(subcode_v, type(subcode_V))
#         if not self.get():
#             print('False')
#             return False
#         else:
#             print('True')
#             return True
#
#     def useless(self, subcode_1, subcode_2):
#         print(subcode_1, subcode_2)
#         print('oh hi mark!')
#         print(self.state())
#         return False
