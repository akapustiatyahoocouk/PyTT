from typing import final

from awt.VirtualKey import VirtualKey
from awt.InputEventModifiers import InputEventModifiers

@final
class KeyStroke:
    
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
        assert isinstance(self, KeyStroke)
        if not isinstance(op2, KeyStroke):
            return False
        return (self.__keycode == op2.__keycode and
                self.__modifiers == op2.__modifiers)

    def __ne__(self, op2: "KeyStroke") -> bool:
        assert isinstance(self, KeyStroke)
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
    def keycode(self) -> InputEventModifiers:
        """ The modifiers of this keystroke, never None. """
        return self.__modifiers
