"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad


# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros"


# CLASSES AND FUNCTIONS ----------------


class App:
    """Class representing a host-side application, for which we have a set
    of macro sequences. Project code was originally more complex and
    this was helpful, but maybe it's excessive now?"""

    def __init__(self, appdata):
        self.name = appdata["name"]
        self.macros = appdata["macros"]

    def switch(self):
        """Activate application settings; update OLED labels and LED
        colors."""
        group[13].text = self.name  # Application name
        for i in range(12):
            if i < len(self.macros):  # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ""
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            anchored_position=(
                (macropad.display.width - 1) * x / 2,
                macropad.display.height - 1 - (3 - y) * 12,
            ),
            anchor_point=(x / 2, 1.0),
        )
    )
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(
    label.Label(
        terminalio.FONT,
        text="",
        color=0x000000,
        anchored_position=(macropad.display.width // 2, -2),
        anchor_point=(0.5, 0.0),
    )
)
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
scenes = {}
files = os.listdir(MACRO_FOLDER)
files.sort()

for filename in files:
    if filename.endswith(".py"):
        try:
            module = __import__(MACRO_FOLDER + "/" + filename[:-3])
            if "id" in module.app:
                scenes[module.app["id"]] = App(module.app)
        except (
            SyntaxError,
            ImportError,
            AttributeError,
            KeyError,
            NameError,
            IndexError,
            TypeError,
        ) as err:
            print("ERROR in", filename)
            import traceback

            traceback.print_exception(err, err, err.__traceback__)

if not scenes:
    group[13].text = "NO MACRO FILES FOUND"
    macropad.display.refresh()
    while True:
        pass

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0

default_scene = "home"
active_scene = default_scene
scenes[active_scene].switch()

# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder
    # if position != last_position:
    #     app_index = position % len(apps)
    #     apps[app_index].switch()
    #     last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(scenes[active_scene].macros) < 13:
            continue  # No 13th macro, just resume main loop
        key_number = 12  # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(scenes[active_scene].macros):
            continue  # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    sequence = scenes[active_scene].macros[key_number][2]

    if pressed:
        if key_number < 12:  # No pixel for encoder button
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        else:
            print("Encoder button pressed")

            active_scene = default_scene
            scenes[active_scene].switch()
            continue

        for item in sequence:
            if not isinstance(item, dict):
                print("item pressed", item)

            if not isinstance(item, dict) or not "type" in item:
                continue

            if item["type"] == "scene":
                dest_scene = item["dest"]

                if not dest_scene in scenes:
                    print("Unknown scene", item["dest"])
                    continue

                active_scene = dest_scene
                scenes[active_scene].switch()
            elif item["type"] == "press":
                for key in item["keys"]:
                    if isinstance(key, int):
                        if key >= 0:
                            macropad.keyboard.press(key)
                        else:
                            macropad.keyboard.release(-key)
                    elif isinstance(key, float):
                        time.sleep(key)
                    elif isinstance(key, str):
                        macropad.keyboard_layout.write(key)

    else:
        # Release any still-pressed keys, consumer codes, mouse buttons
        # Keys and mouse buttons are individually released this way (rather
        # than release_all()) because pad supports multi-key rollover, e.g.
        # could have a meta key or right-mouse held down by one macro and
        # press/release keys/buttons with others. Navigate popups, etc.
        for item in sequence:
            if not isinstance(item, dict):
                print("item pressed", item)

            if not isinstance(item, dict) or not "type" in item:
                continue

            if item["type"] == "press":
                for key in item["keys"]:
                    if isinstance(key, int):
                        if key >= 0:
                            macropad.keyboard.release(key)

        macropad.consumer_control.release()

        if key_number < 12:  # No pixel for encoder button
            macropad.pixels[key_number] = scenes[active_scene].macros[key_number][0]
            macropad.pixels.show()
