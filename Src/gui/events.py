from abc import ABC, ABCMeta
from typing import Any, Optional, final
from enum import Enum
import re
import tkinter as tk

@final
class VirtualKey(Enum):
    """ The keyboard key ID. """

    ##########
    #   Virtual key codes

    #   ASCII
    VK_0 = ord('0')
    VK_1 = ord('1')
    VK_2 = ord('2')
    VK_3 = ord('3')
    VK_4 = ord('4')
    VK_5 = ord('5')
    VK_6 = ord('6')
    VK_7 = ord('7')
    VK_8 = ord('8')
    VK_9 = ord('9')

    VK_A = ord('A')
    VK_B = ord('B')
    VK_C = ord('C')
    VK_D = ord('D')
    VK_E = ord('E')
    VK_F = ord('F')
    VK_G = ord('G')
    VK_H = ord('H')
    VK_I = ord('I')
    VK_J = ord('J')
    VK_K = ord('K')
    VK_L = ord('L')
    VK_M = ord('M')
    VK_N = ord('N')
    VK_O = ord('O')
    VK_P = ord('P')
    VK_Q = ord('Q')
    VK_R = ord('R')
    VK_S = ord('S')
    VK_T = ord('T')
    VK_U = ord('U')
    VK_V = ord('V')
    VK_W = ord('W')
    VK_X = ord('X')
    VK_Y = ord('Y')
    VK_Z = ord('Z')
    
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
    
    #   Misc.
    VK_NONE = 0

    ##########
    #   Implementation
    
    ##########
    #   Operations
    @staticmethod
    def from_tk_string(key_string: str) -> 'VirtualKey':
        """ Parses a Tk - style key name, returning the corresponging virtual key. """
        if key_string in _key_map:
            return _key_map[key_string]
        return VirtualKey.VK_NONE

_key_map = { 
    #   ASCII
    '0': VirtualKey.VK_0,
    '1': VirtualKey.VK_1,
    '2': VirtualKey.VK_2,
    '3': VirtualKey.VK_3,
    '4': VirtualKey.VK_4,
    '5': VirtualKey.VK_5,
    '6': VirtualKey.VK_6,
    '7': VirtualKey.VK_7,
    '8': VirtualKey.VK_8,
    '9': VirtualKey.VK_9,

    'a': VirtualKey.VK_A,
    'A': VirtualKey.VK_A,
    'b': VirtualKey.VK_B,
    'B': VirtualKey.VK_B,
    'c': VirtualKey.VK_C,
    'C': VirtualKey.VK_C,
    'd': VirtualKey.VK_D,
    'D': VirtualKey.VK_D,
    'e': VirtualKey.VK_E,
    'E': VirtualKey.VK_E,
    'f': VirtualKey.VK_F,
    'F': VirtualKey.VK_F,
    'g': VirtualKey.VK_G,
    'G': VirtualKey.VK_G,
    'h': VirtualKey.VK_H,
    'H': VirtualKey.VK_H,
    'i': VirtualKey.VK_I,
    'I': VirtualKey.VK_I,
    'j': VirtualKey.VK_J,
    'J': VirtualKey.VK_J,
    'k': VirtualKey.VK_K,
    'K': VirtualKey.VK_K,
    'l': VirtualKey.VK_L,
    'L': VirtualKey.VK_L,
    'm': VirtualKey.VK_M,
    'M': VirtualKey.VK_M,
    'n': VirtualKey.VK_N,
    'N': VirtualKey.VK_N,
    'o': VirtualKey.VK_O,
    'O': VirtualKey.VK_O,
    'p': VirtualKey.VK_P,
    'P': VirtualKey.VK_P,
    'q': VirtualKey.VK_Q,
    'Q': VirtualKey.VK_Q,
    'r': VirtualKey.VK_R,
    'R': VirtualKey.VK_R,
    's': VirtualKey.VK_S,
    'S': VirtualKey.VK_S,
    't': VirtualKey.VK_T,
    'T': VirtualKey.VK_T,
    'u': VirtualKey.VK_U,
    'U': VirtualKey.VK_U,
    'v': VirtualKey.VK_V,
    'V': VirtualKey.VK_V,
    'w': VirtualKey.VK_W,
    'W': VirtualKey.VK_W,
    'x': VirtualKey.VK_X,
    'X': VirtualKey.VK_X,
    'y': VirtualKey.VK_Y,
    'Y': VirtualKey.VK_Y,
    'z': VirtualKey.VK_Z,
    'Z': VirtualKey.VK_Z,

    #   Non-ASCII
    'F1': VirtualKey.VK_F1,
    'F2': VirtualKey.VK_F2,
    'F3': VirtualKey.VK_F3,
    'F4': VirtualKey.VK_F4,
    'F5': VirtualKey.VK_F5,
    'F6': VirtualKey.VK_F6,
    'F7': VirtualKey.VK_F7,
    'F8': VirtualKey.VK_F8,
    'F9': VirtualKey.VK_F9,
    'F10': VirtualKey.VK_F10,
    'F11': VirtualKey.VK_F11,
    'F12': VirtualKey.VK_F12,
    
    #   Terminator
    '<<no way!!!>': VirtualKey.VK_NONE
    }

class Event(ABC):
    """ The common base class for all events. """

    ##########
    #   Construction
    def __init__(self, source):
        """ Constructs the event with the specified source. """
        self.__source = source
        
    ##########
    #   Properties
    @property
    def source(self) -> Any:
        """ The source that has raised this event. """
        return self.__source

class InputEventMeta(ABCMeta):  # TODO rename ?
    def __setattr__(cls: type, attr: str, value) -> None:
        #print(cls.__name__, attr, value)
        if re.match('^[A-Z0-9_]+$', attr):
            raise Exception('Cannot change class constant value ' + cls.__name__ + '.' + attr)
        type.__setattr__(cls, attr, value)

class InputEvent(Event, metaclass=InputEventMeta):
    """ A generic user input event. """

    ##########
    #   Constants
    MODIFIER_SHIFT : int = 0x00000001
    MODIFIER_LOCK : int = 0x00000002
    MODIFIER_CONTROL : int = 0x00000004
    #        mods = ('Shift', 'Lock', 'Control',
    #                'Mod1', 'Mod2', 'Mod3', 'Mod4', 'Mod5',
    #                'Button1', 'Button2', 'Button3', 'Button4', 'Button5')
    MODIFIER_ALT : int = 0x00020000
    MODIFIER_NUMPAD : int = 0x00040000
    
    ##########
    #   Construction
    def __init__(self, source, modifiers=None):
        """ Constructs the event with the specified source and modifiers. """
        super().__init__(source)
        
        assert (modifiers is None) or isinstance(modifiers, int)
        self.__modifiers = 0 if (modifiers is None) else modifiers

    ##########
    #   Properties
    @property
    def modifiers(self: Any):
        """ The modifiers active at the time this event was raised. """
        return self.__modifiers

    @property
    def modifiers_string(self) -> str:
        result = ''
        if (self.modifiers & InputEvent.MODIFIER_SHIFT) != 0:
            result += 'Shift+'
        if (self.modifiers & InputEvent.MODIFIER_LOCK) != 0:
            result += 'Lock+'
        if (self.modifiers & InputEvent.MODIFIER_CONTROL) != 0:
            result += 'Control+'
        if (self.modifiers & InputEvent.MODIFIER_ALT) != 0:
            result += 'Alt+'
        if (self.modifiers & InputEvent.MODIFIER_NUMPAD) != 0:
            result += 'NumPad+'
        return result if len(result) == 0 else result[:len(result)-1]


class KeyEvent(InputEvent):
    """ A generic key input event. """

    ##########
    #   Construction
    def __init__(self, source, tk_evt: tk.Event):
        """ Constructs the event from the specified tk key event. """
        super().__init__(source, tk_evt.state)
        
        if (tk_evt.char is not None) and (len(tk_evt.char) == 1):
            self.__keychar = tk_evt.char[0]
        else:
            self.__keychar = None
            
        self.__keycode = VirtualKey.from_tk_string(tk_evt.keysym)

    #def __init__(self, source, keycode: VirtualKey = None, keychar=None, modifiers=None):
    #    """ Constructs the event with the specified source and modifiers. """
    #    super().__init__(source, modifiers)
        
    #    assert (keycode is None) or isinstance(keycode, VirtualKey)
    #    self.__keycode = VirtualKey.VK_NONE if (keycode is None) else keycode

    #    assert (keychar is None) or isinstance(keychar, str)
    #    self.__keychar = keychar

    ##########
    #   object
    def __str__(self) -> str:
        result = ''
        if self.source is not None:
            result += 'source='
            result += str(self.source)
            result += ','
        if len(self.modifiers_string) > 0:
            result += 'modifiers='
            result += self.modifiers_string
            result += ','
        if self.keycode is not None:
            result += 'keycode='
            result += str(self.keycode)
            result += ','
        if self.keychar is not None:
            result += 'keychar='
            result += self.keychar
            result += ','
        if result.endswith(','):
            result = result[:len(result)-1]
        return 'KeyEvent(' + result + ')'
    
    @property
    def keycode(self) -> VirtualKey:
        """ The virtual key code, None if not known. """
        return self.__keycode

    @property
    def keychar(self) -> Optional[str]:
        """ The key character, None if not known. """
        return self.__keychar
