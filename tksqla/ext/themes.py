THEMES = {
    'Dark': {
        'parent': 'vista',
        'settings': {
            'TButton': {
                'configure': {
                    'foreground': 'red',
                    'background': 'black'
                }
            }
        }
    },
    'HighContrast': {
        'parent': 'vista',
        'settings': {
            'TButton': {
                'configure': {
                    'foreground': 'black',
                    'background': 'white'
                }
            }
        }
    }
}

"""
class DarkTheme:
    def __init__(self):
        style = ttk.Style()
        style.configure('TEST.TButton', foreground='red', background='black')

        style.theme_create('DarkMode', 'vista')
        style.theme_settings('DarkMode', {
            'TButton': {
                'configure': {
                    'foreground': 'red',
                    'background': 'black'
                }
            }
        })
        print(style.theme_names())
        style.theme_use('DarkMode')
"""
