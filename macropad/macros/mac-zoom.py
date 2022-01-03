# MACROPAD Hotkeys example: Safari web browser for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Mac Zoom', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        # 2nd row ----------
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        # 3rd row ----------
        (0x004000, 'Video', [Keycode.COMMAND, Keycode.SHIFT, 'v']),
        (0x000000, '', []),
        (0x000000, '', []),
        # 4th row ----------
        (0x004000, 'Audio', [Keycode.COMMAND, Keycode.SHIFT, 'a']),
        (0x000000, '', []),
        (0x400000, 'End', [Keycode.COMMAND, 'w', 0.5, Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', []),
    ]
}
