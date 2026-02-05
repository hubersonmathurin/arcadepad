import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Macros, Release, Tap
from kmk.modules.encoder import EncoderHandler
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.layers import Layers
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306


layer: int = 0

i2c_bus = busio.I2C(board.GP7, board.GP6)

driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
    # Optional:
    device_address=0x3C,
)

keyboard.modules.append(Layers())
encoder_handler = EncoderHandler()
keyboard = KMKKeyboard()
macros = Macros()
keyboard.modules.append(MouseKeys())
mousekeys = MouseKeys(
    max_speed = 10,
    acc_interval = 20, # Delta ms to apply acceleration
    move_step = 1
)
keyboard.modules.append(macros)
keyboard.modules = [layers, holdtap, encoder_handler]

PINS = [board.GP26, board.GP27, board.GP29, board.GP28, board.GP0, board.GP3]

encoder_handler.pins = (
    (board.GP2, board.GP1, board.GP4,), 
)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)


keyboard.matrix = KeysScanner(
    rows=PINS, 
    value_when_pressed=False,
)

keyboard.keymap = [
    #3D-1
    [
        KC.MACRO("ssketch" + KC.ENTER),	KC.C,	KC.F,
        KC.MACRO("schamfer" + KC.ENTER),	KC.MACRO("sshell" + KC.ENTER),	KC.MACRO("sloft" + KC.ENTER),
    ]
    #3D-2
    [
        KC.MACRO("srevolve" + KC.ENTER),	KC.MACRO("ssweep" + KC.ENTER),	KC.J,
        KC.MACRO("srect" + KC.ENTER),	KC.MACRO("scirc" + KC.ENTER),	KC.M,
    ]  
    #2D
    [
        KC.C, KC.MACRO("scircle" + KC.ENTER), KC.MACRO("smirror" + KC.ENTER),
        KC.MACRO("soffest" + KC.ENTER), KC.L, KC.R,
    ]
]

display.entries = [
    TextEntry(text="3D-1", x=64, y=0, x_anchor="M", y_anchor="T", layer = 0), # text in Top Right corner
    TextEntry(text="3D-2", x=64, y=0, x_anchor="M", y_anchor="T", layer = 1), # text in Bottom Right corner
    TextEntry(text="2D", x=64, y=0, x_anchor="M", y_anchor="T", layer = 2), # text in the Middle of screen

    TextEntry(text="SKETCH", x=0, y=64, x_anchor="L", y_anchor="M", layer = 0),
    TextEntry(text="EXTRUDE", x=64, y=64, x_anchor="M", y_anchor="M", layer = 0),
    TextEntry(text="FILLET", x=128, y=64, x_anchor="R", y_anchor="M", layer = 0),
    TextEntry(text="CHAMFER", x=0, y=128, x_anchor="L", y_anchor="B", layer = 0),
    TextEntry(text="SHELL", x=64, y=128, x_anchor="M", y_anchor="B", layer = 0),
    TextEntry(text="LOFT", x=128, y=128, x_anchor="R", y_anchor="B", layer = 0),

    TextEntry(text="REVOLVE", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),
    TextEntry(text="SWEEP", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),
    TextEntry(text="JOINT", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),
    TextEntry(text="RPATTERN", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),
    TextEntry(text="CPATTERN", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),
    TextEntry(text="MOVE", x=0, y=64, x_anchor="L", y_anchor="M", layer = 1),

    TextEntry(text="CIRCLE", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
    TextEntry(text="2PTCIRCLE", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
    TextEntry(text="MIRROR", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
    TextEntry(text="OFFSET", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
    TextEntry(text="LINE", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
    TextEntry(text="RECT", x=0, y=64, x_anchor="L", y_anchor="M", layer = 2),
]

keyboard.extensions.append(display)

encoder_handler.map = [
    KC.MW_UP, KC.MW_DOWN, KC.NEXTLAYER
]

def next_layer():
    global layer
    layer = (layer + 1) % len(keyboard.keymap)
    keyboard.current_layer = layer
  
KC_NEXTLAYER = make_key(
    names=('KC_NEXTLAYER',),
    on_press=next_layer,
)
