""" Specifies the key stroke that can be performed by the user, """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import final

#   Internal dependencies on modules within the same component
from .VirtualKey import VirtualKey
from .InputEventModifiers import InputEventModifiers

##########
#   Public entities
@final
class KeyStroke:
    """ Specifies the key stroke that can be performed by the user, """

    ##########
    #   Construction
    def __init__(self,
                 keycode: VirtualKey,
                 modifiers: InputEventModifiers = InputEventModifiers.NONE) -> None:
        assert isinstance(keycode, VirtualKey)
        assert keycode is not VirtualKey.VK_NONE
        assert modifiers is not None

        self.__keycode = keycode
        self.__modifiers = modifiers

    ##########
    #   object
    def __repr__(self):
        ms = repr(self.__modifiers)
        return (repr(self.__keycode) if len(ms) == 0
                else ms + "+" + repr(self.__keycode))

    def __str__(self):
        ms = str(self.__modifiers)
        return (str(self.__keycode) if len(ms) == 0
                else ms + "+" + str(self.__keycode))

    def __eq__(self, op2: "KeyStroke") -> bool:
        if not isinstance(op2, KeyStroke):
            return False
        return (self.__keycode == op2.__keycode and
                self.__modifiers == op2.__modifiers)

    def __ne__(self, op2: "KeyStroke") -> bool:
        if not isinstance(op2, KeyStroke):
            return True
        return (self.__keycode != op2.__keycode or
                self.__modifiers != op2.__modifiers)

    ##########
    #   Properties
    @property
    def keycode(self) -> VirtualKey:
        """ The virtual key code of this keystroke, never None. """
        return self.__keycode

    @property
    def modifiers(self) -> InputEventModifiers:
        """ The modifiers of this keystroke, never None. """
        return self.__modifiers

    ##########
    #  Operations
    @staticmethod
    def parse(s: str) -> KeyStroke:
        """
            Parses a string representation of a KeyStroke (in the
            form Ctrl+Shift+Alt+N, etc.)

            @param s:
                The string representation of a KeyStroke.
            @return:
                The parsed KeyStroke specification.
            @raise ValueError:
                If the specified string is not a valid KeyStroke
                specification.
        """
        assert isinstance(s, str)

        #   Consume modifiers
        modifiers = InputEventModifiers.NONE
        modifiers_map = {
            str(InputEventModifiers.CONTROL).lower(): InputEventModifiers.CONTROL,
            str(InputEventModifiers.SHIFT).lower(): InputEventModifiers.SHIFT,
            str(InputEventModifiers.ALT).lower(): InputEventModifiers.ALT}
        keep_going = True
        while keep_going:
            keep_going = False
            #   Does "s" start with "<modifier>+" ?
            for (key, value) in modifiers_map.items():
                prefix = key + "+"
                if s.lower().startswith(prefix):
                    s = s[len(prefix):]
                    modifiers |= value
                    keep_going = True
                    break
        #   Consume virtual key
        for vk in VirtualKey:
            if str(vk).lower() == s.lower():
                return KeyStroke(vk, modifiers)
        raise ValueError("Invalid KeyStroke specification'" + s + "'")
