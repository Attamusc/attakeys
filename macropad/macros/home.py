# Starting layout for macropad

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

app = {  # REQUIRED dict, must be named 'app'
    "id": "home",
    "name": "Home",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x202000, "Safari", [{"type": "scene", "dest": "safari"}]),
        (0x202000, "Zoom", [{"type": "scene", "dest": "zoom"}]),
        (0x202000, "Media", [{"type": "scene", "dest": "media"}]),
        # 2nd row ----------
        (0x202000, "Mouse", [{"type": "scene", "dest": "mouse"}]),
        (0x000000, "", []),
        (0x202000, "Tones", [{"type": "scene", "dest": "tones"}]),
        # 3rd row ----------
        (0x202000, "Numpad", [{"type": "scene", "dest": "numpad"}]),
        (0x000000, "", []),
        (0x000000, "", []),
        # 4th row ----------
        (
            0x000020,
            "Raycast",
            [{"type": "press", "keys": [Keycode.COMMAND, " "]}],
        ),
        (0x000000, "", []),
        (
            0x000020,
            "1Password",
            [{"type": "press", "keys": [Keycode.COMMAND, Keycode.SHIFT, "x"]}],
        ),
        # Encoder button ---
        (0x000000, "", []),
    ],
}
