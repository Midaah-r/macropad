# Import necessary libraries
import board
import displayio
import terminalio
from adafruit_display_text import label
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.oled import Oled, OledDisplayMode, OledReactionType, OledData

# Keyboard instance
keyboard = KMKKeyboard()

# --- OLED Configuration ---
display = board.DISPLAY  # Initialize display
oled_text_area = label.Label(terminalio.FONT, text="Macropad Ready", color=0xFFFFFF, x=8, y=8)
display.show(oled_text_area)

oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC, 1:["Macropad v1"]},
        corner_two={0:OledReactionType.LAYER, 1:["Layer: 0", "Layer: 1"]},
        corner_three={0:OledReactionType.LAYER, 1:["Media", "Macros"]},
        corner_four={0:OledReactionType.LAYER, 1:["Vol: 50%", "Macros"]},
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False
)
keyboard.extensions.append(oled_ext)

# --- Rotary Encoder ---
encoder_handler = EncoderHandler()
encoder_handler.pins = (
    (board.D6, board.D7, board.D8, True),  # Encoder 1: CLK, DT, SW, is_inverted
)
keyboard.modules.append(encoder_handler)

# --- Macros ---
macros = Macros()
keyboard.modules.append(macros)

# Key pins (adjust according to your wiring)
PINS = [
    board.D0, board.D1, board.D2, 
    board.D3, board.D4, board.D5,
    board.D9, board.D10, board.D11,
    board.D12, board.D13, board.D14
]

# Keyboard matrix setup
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Keymap layers
keyboard.keymap = [
    # Layer 0: Media controls
    [
        KC.MPLY, KC.MNXT, KC.MPRV,
        KC.VOLD, KC.VOLU, KC.MUTE,
        KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.Z),
        KC.MACRO("Hello!"), KC.LCTL(KC.Y), KC.LCTL(KC.S)
    ],
    
    # Layer 1: Macros and functions
    [
        KC.F13, KC.F14, KC.F15,
        KC.F16, KC.F17, KC.F18,
        KC.MACRO("email@example.com"), KC.MACRO("MyPassword123"), KC.MACRO("sudo reboot"),
        KC.TO(0), KC.RGB_TOG, KC.RGB_MODE_PLAIN
    ]
]

# Encoder mappings (adjust for your needs)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Layer 0
    ((KC.LEFT, KC.RIGHT, KC.ENTER),)  # Layer 1
]

# RGB Configuration (if you have RGB)
if hasattr(board, 'NEOPIXEL'):
    from kmk.extensions.RGB import RGB
    rgb = RGB(pixel_pin=board.NEOPIXEL, num_pixels=12)
    keyboard.extensions.append(rgb)

# Start the keyboard
if __name__ == '__main__':
    keyboard.go()