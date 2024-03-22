from abc import ABCMeta
from typing import Any
import re

import awt_impl.Event

class _InputEventMeta(ABCMeta):  # TODO rename ?
    def __setattr__(cls: type, attr: str, value) -> None:
        #print(cls.__name__, attr, value)
        if re.match("^[A-Z0-9_]+$", attr):
            raise Exception("Cannot change class constant value " + cls.__name__ + "." + attr)
        type.__setattr__(cls, attr, value)

class InputEvent(awt_impl.Event.Event, metaclass=_InputEventMeta):
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
        result = ""
        if (self.modifiers & InputEvent.MODIFIER_SHIFT) != 0:
            result += "Shift+"
        if (self.modifiers & InputEvent.MODIFIER_LOCK) != 0:
            result += "Lock+"
        if (self.modifiers & InputEvent.MODIFIER_CONTROL) != 0:
            result += "Control+"
        if (self.modifiers & InputEvent.MODIFIER_ALT) != 0:
            result += "Alt+"
        if (self.modifiers & InputEvent.MODIFIER_NUMPAD) != 0:
            result += "NumPad+"
        return result if len(result) == 0 else result[:len(result)-1]

