""" Defines abstract IDs for keyboard keys. """

#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class VirtualKey(Enum):
    """ The keyboard key ID. """

    ##########
    #   Virtual key codes

    #   ASCII control
    VK_BACKSPACE = 8
    VK_TAB = 9
    VK_RETURN = 13
    VK_ESCAPE = 27

    #   ASCII
    VK_SPACE = ord(" ")

    VK_DOT = ord(".")
    VK_PLUS = ord("+")
    VK_MINUS = ord("-")
    VK_ASTERISK = ord("*")
    VK_SLASH = ord("/")
    VK_GRAVE = ord("`")
    VK_TILDE = ord("~")
    VK_EXCLAMATION = ord("!")
    VK_AT = ord("@")
    VK_HASH = ord("#")
    VK_DOLLAR = ord("$")
    VK_PERCENT = ord("%")
    VK_CIRCUM = ord("^")
    VK_AMPERSAND = ord("&")
    VK_OPENING_PARENTHESIS = ord("(")
    VK_CLOSING_PARENTHESIS = ord(")")
    VK_UNDERSCORE = ord("_")
    VK_EQUALS = ord("=")
    VK_SEMICOLON = ord(";")
    VK_COLON = ord(":")
    VK_APOSTROPHE = ord("'")
    VK_QUOTE = ord("\"")
    VK_BACKSLASH = ord("\\")
    VK_BAR = ord("|")
    VK_COMMA = ord(",")
    VK_LESS = ord("<")
    VK_GREATER = ord("?")
    VK_QUESTION = ord("?")
    VK_OPENING_BRACKET = ord("[")
    VK_CLOSING_BRACKET = ord("]")
    VK_OPENING_BRACE = ord("{")
    VK_CLOSING_BRACE = ord("}")

    VK_0 = ord("0")
    VK_1 = ord("1")
    VK_2 = ord("2")
    VK_3 = ord("3")
    VK_4 = ord("4")
    VK_5 = ord("5")
    VK_6 = ord("6")
    VK_7 = ord("7")
    VK_8 = ord("8")
    VK_9 = ord("9")

    VK_A = ord("A")
    VK_B = ord("B")
    VK_C = ord("C")
    VK_D = ord("D")
    VK_E = ord("E")
    VK_F = ord("F")
    VK_G = ord("G")
    VK_H = ord("H")
    VK_I = ord("I")
    VK_J = ord("J")
    VK_K = ord("K")
    VK_L = ord("L")
    VK_M = ord("M")
    VK_N = ord("N")
    VK_O = ord("O")
    VK_P = ord("P")
    VK_Q = ord("Q")
    VK_R = ord("R")
    VK_S = ord("S")
    VK_T = ord("T")
    VK_U = ord("U")
    VK_V = ord("V")
    VK_W = ord("W")
    VK_X = ord("X")
    VK_Y = ord("Y")
    VK_Z = ord("Z")

    #   Non-ASCII
    VK_F1 = 0x00010001
    VK_F2 = 0x00010002
    VK_F3 = 0x00010003
    VK_F4 = 0x00010004
    VK_F5 = 0x00010005
    VK_F6 = 0x00010006
    VK_F7 = 0x00010007
    VK_F8 = 0x00010008
    VK_F9 = 0x00010009
    VK_F10 = 0x0001000A
    VK_F11 = 0x0001000B
    VK_F12 = 0x0001000C

    VK_CONTROL = 0x00010010
    VK_SHIFT = 0x00010011
    VK_ALT = 0x00010012
    VK_APP = 0x00010013
    VK_CAPS_LOCK = 0x00010014
    VK_SCROLL_LOCK = 0x00010015
    VK_NUM_LOCK = 0x00010016
    VK_PAUSE = 0x00010017
    #   VK_PRINT_SCREEN

    VK_UP = 0x00010020
    VK_DOWN = 0x00010021
    VK_LEFT = 0x00010022
    VK_RIGHT = 0x00010023
    VK_PRIOR = 0x00010024
    VK_NEXT = 0x00010025
    VK_HOME = 0x00010026
    VK_END = 0x00010027
    VK_INSERT = 0x00010028
    VK_DELETE = 0x00010029

    #   Misc.
    VK_NONE = 0

    ##########
    #   object
    def __str__(self) -> str:
        return _str_map.get(self, _str_map[VirtualKey.VK_NONE])

    ##########
    #   Operations
    @staticmethod
    def from_tk_string(key_string: str) -> "VirtualKey":
        """ Parses a Tk - style key name, returning the corresponging virtual key. """
        if key_string in _key_map:
            return _key_map[key_string]
        return VirtualKey.VK_NONE

_key_map = {
    #   ASCII control
    "BackSpace": VirtualKey.VK_BACKSPACE,
    "Tab": VirtualKey.VK_TAB,
    "Return": VirtualKey.VK_RETURN,
    "Escape": VirtualKey.VK_ESCAPE,

    #   ASCII
    "space": VirtualKey.VK_SPACE,

    "period": VirtualKey.VK_DOT,
    "plus": VirtualKey.VK_PLUS,
    "minus": VirtualKey.VK_MINUS,
    "asterisk": VirtualKey.VK_ASTERISK,
    "slash": VirtualKey.VK_SLASH,
    "grave": VirtualKey.VK_GRAVE,
    "asciitilde": VirtualKey.VK_TILDE,
    "exclam": VirtualKey.VK_EXCLAMATION,
    "at": VirtualKey.VK_AT,
    "numbersign": VirtualKey.VK_HASH,
    "dollar": VirtualKey.VK_DOLLAR,
    "percent": VirtualKey.VK_PERCENT,
    "asciicircum": VirtualKey.VK_CIRCUM,
    "ampersand": VirtualKey.VK_AMPERSAND,
    "parenleft": VirtualKey.VK_OPENING_PARENTHESIS,
    "parenright": VirtualKey.VK_CLOSING_PARENTHESIS,
    "underscore": VirtualKey.VK_UNDERSCORE,
    "equal": VirtualKey.VK_EQUALS,
    "semicolon": VirtualKey.VK_SEMICOLON,
    "colon": VirtualKey.VK_COLON,
    "apostrophe": VirtualKey.VK_APOSTROPHE,
    "quotedbl": VirtualKey.VK_QUOTE,
    "backslash": VirtualKey.VK_BACKSLASH,
    "bar": VirtualKey.VK_BAR,
    "comma": VirtualKey.VK_COMMA,
    "less": VirtualKey.VK_LESS,
    "greater": VirtualKey.VK_GREATER,
    "question": VirtualKey.VK_QUESTION,
    "bracketleft": VirtualKey.VK_OPENING_BRACKET,
    "braceleft": VirtualKey.VK_OPENING_BRACE,
    "bracketright": VirtualKey.VK_CLOSING_BRACKET,
    "braceright": VirtualKey.VK_CLOSING_BRACE,

    "0": VirtualKey.VK_0,
    "1": VirtualKey.VK_1,
    "2": VirtualKey.VK_2,
    "3": VirtualKey.VK_3,
    "4": VirtualKey.VK_4,
    "5": VirtualKey.VK_5,
    "6": VirtualKey.VK_6,
    "7": VirtualKey.VK_7,
    "8": VirtualKey.VK_8,
    "9": VirtualKey.VK_9,

    "a": VirtualKey.VK_A,
    "A": VirtualKey.VK_A,
    "b": VirtualKey.VK_B,
    "B": VirtualKey.VK_B,
    "c": VirtualKey.VK_C,
    "C": VirtualKey.VK_C,
    "d": VirtualKey.VK_D,
    "D": VirtualKey.VK_D,
    "e": VirtualKey.VK_E,
    "E": VirtualKey.VK_E,
    "f": VirtualKey.VK_F,
    "F": VirtualKey.VK_F,
    "g": VirtualKey.VK_G,
    "G": VirtualKey.VK_G,
    "h": VirtualKey.VK_H,
    "H": VirtualKey.VK_H,
    "i": VirtualKey.VK_I,
    "I": VirtualKey.VK_I,
    "j": VirtualKey.VK_J,
    "J": VirtualKey.VK_J,
    "k": VirtualKey.VK_K,
    "K": VirtualKey.VK_K,
    "l": VirtualKey.VK_L,
    "L": VirtualKey.VK_L,
    "m": VirtualKey.VK_M,
    "M": VirtualKey.VK_M,
    "n": VirtualKey.VK_N,
    "N": VirtualKey.VK_N,
    "o": VirtualKey.VK_O,
    "O": VirtualKey.VK_O,
    "p": VirtualKey.VK_P,
    "P": VirtualKey.VK_P,
    "q": VirtualKey.VK_Q,
    "Q": VirtualKey.VK_Q,
    "r": VirtualKey.VK_R,
    "R": VirtualKey.VK_R,
    "s": VirtualKey.VK_S,
    "S": VirtualKey.VK_S,
    "t": VirtualKey.VK_T,
    "T": VirtualKey.VK_T,
    "u": VirtualKey.VK_U,
    "U": VirtualKey.VK_U,
    "v": VirtualKey.VK_V,
    "V": VirtualKey.VK_V,
    "w": VirtualKey.VK_W,
    "W": VirtualKey.VK_W,
    "x": VirtualKey.VK_X,
    "X": VirtualKey.VK_X,
    "y": VirtualKey.VK_Y,
    "Y": VirtualKey.VK_Y,
    "z": VirtualKey.VK_Z,
    "Z": VirtualKey.VK_Z,

    #   Non-ASCII
    "F1": VirtualKey.VK_F1,
    "F2": VirtualKey.VK_F2,
    "F3": VirtualKey.VK_F3,
    "F4": VirtualKey.VK_F4,
    "F5": VirtualKey.VK_F5,
    "F6": VirtualKey.VK_F6,
    "F7": VirtualKey.VK_F7,
    "F8": VirtualKey.VK_F8,
    "F9": VirtualKey.VK_F9,
    "F10": VirtualKey.VK_F10,
    "F11": VirtualKey.VK_F11,
    "F12": VirtualKey.VK_F12,

    "Control_L": VirtualKey.VK_CONTROL,
    "Control_R": VirtualKey.VK_CONTROL,
    "Shift_L": VirtualKey.VK_SHIFT,
    "Shift_R": VirtualKey.VK_SHIFT,
    "Alt_L": VirtualKey.VK_ALT,
    "Alt_R": VirtualKey.VK_ALT,
    "App": VirtualKey.VK_APP,
    "Caps_Lock": VirtualKey.VK_CAPS_LOCK,
    "Scroll_Lock": VirtualKey.VK_SCROLL_LOCK,
    "Num_Lock": VirtualKey.VK_NUM_LOCK,
    "Pause": VirtualKey.VK_PAUSE,

    "Up": VirtualKey.VK_UP,
    "Down": VirtualKey.VK_DOWN,
    "Left": VirtualKey.VK_LEFT,
    "Right": VirtualKey.VK_RIGHT,
    "Prior": VirtualKey.VK_PRIOR,
    "Next": VirtualKey.VK_NEXT,
    "Home": VirtualKey.VK_HOME,
    "End": VirtualKey.VK_END,
    "Insert": VirtualKey.VK_INSERT,
    "Delete": VirtualKey.VK_DELETE,

    #   Terminator
    "<Unknown key>": VirtualKey.VK_NONE
    }

#   Build str(vk) response map
_str_map = {}
for (k, v) in _key_map.items():
    _str_map[v] = k
_str_map[VirtualKey.VK_SPACE] = " "
_str_map[VirtualKey.VK_DOT] = "."
_str_map[VirtualKey.VK_PLUS] = "+"
_str_map[VirtualKey.VK_MINUS] = "-"
_str_map[VirtualKey.VK_ASTERISK] = "*"
_str_map[VirtualKey.VK_SLASH] = "/"
_str_map[VirtualKey.VK_GRAVE] = "`"
_str_map[VirtualKey.VK_TILDE] = "~"
_str_map[VirtualKey.VK_EXCLAMATION] = "!"
_str_map[VirtualKey.VK_AT] = "@"
_str_map[VirtualKey.VK_HASH] = "#"
_str_map[VirtualKey.VK_DOLLAR] = "$"
_str_map[VirtualKey.VK_PERCENT] = "%"
_str_map[VirtualKey.VK_CIRCUM] = "^"
_str_map[VirtualKey.VK_AMPERSAND] = "&"
_str_map[VirtualKey.VK_OPENING_PARENTHESIS] = "("
_str_map[VirtualKey.VK_CLOSING_PARENTHESIS] = ")"
_str_map[VirtualKey.VK_UNDERSCORE] = "_"
_str_map[VirtualKey.VK_EQUALS] = "="
_str_map[VirtualKey.VK_SEMICOLON] = ";"
_str_map[VirtualKey.VK_COLON] = ":"
_str_map[VirtualKey.VK_APOSTROPHE] = "'"
_str_map[VirtualKey.VK_QUOTE] = "\""
_str_map[VirtualKey.VK_BACKSLASH] = "\\"
_str_map[VirtualKey.VK_BAR] = "|"
_str_map[VirtualKey.VK_COMMA] = ","
_str_map[VirtualKey.VK_LESS] = "<"
_str_map[VirtualKey.VK_GREATER] = ">"
_str_map[VirtualKey.VK_GREATER] = "?"
_str_map[VirtualKey.VK_OPENING_BRACKET] = "["
_str_map[VirtualKey.VK_OPENING_BRACE] = "{"
_str_map[VirtualKey.VK_CLOSING_BRACKET] = "]"
_str_map[VirtualKey.VK_CLOSING_BRACE] = "}"
_str_map[VirtualKey.VK_CONTROL] = "Ctrl"
_str_map[VirtualKey.VK_SHIFT] = "Shift"
_str_map[VirtualKey.VK_ALT] = "Alt"
_str_map[VirtualKey.VK_APP] = "App"
_str_map[VirtualKey.VK_CAPS_LOCK] = "Caps Lock"
_str_map[VirtualKey.VK_SCROLL_LOCK] = "Scroll Lock"
_str_map[VirtualKey.VK_NUM_LOCK] = "Num Lock"
_str_map[VirtualKey.VK_PAUSE] = "Pause"
_str_map[VirtualKey.VK_NONE] = "<Unknown key>"
