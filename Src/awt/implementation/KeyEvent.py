#   Python standard library
from typing import Optional, TypeAlias, Callable
import tkinter as tk

#   Internal dependencies on modules within the same component
from .InputEventModifiers import InputEventModifiers
from .InputEvent import InputEvent
from .VirtualKey import VirtualKey
from .KeyEventType import KeyEventType

##########
#   Public entities
class KeyEvent(InputEvent):
    """ A key input event. """

    ##########
    #   Construction
    def __init__(self, source, event_type: KeyEventType, tk_evt: tk.Event):
        """ Constructs the event from the specified tk key event. """
        super().__init__(source, InputEventModifiers(tk_evt.state))
        
        assert ((event_type is KeyEventType.KEY_DOWN) or
                (event_type is KeyEventType.KEY_UP) or
                (event_type is KeyEventType.KEY_CHAR))
        self.__event_type = event_type

        assert isinstance(tk_evt, tk.Event)
        if ((tk_evt.char is not None) and (len(tk_evt.char) == 1) and
            (ord(tk_evt.char[0]) >= 32) and (ord(tk_evt.char[0]) != 127)):
            self.__keychar = tk_evt.char[0]
        else:
            self.__keychar = None
            
        self.__keycode = VirtualKey.from_tk_string(tk_evt.keysym)

    ##########
    #   object
    def __str__(self) -> str:
        result = ""
        if self.source is not None:
            result += "source="
            result += str(self.source)
            result += ","

        result += "event_type="
        result += str(self.__event_type)
        result += ","

        if len(str(self.modifiers)) > 0:
            result += "modifiers="
            result += str(self.modifiers)
            result += ","

        if self.keycode is not None:
            result += "keycode="
            result += str(self.keycode)
            result += ","

        if self.keychar is not None:
            result += "keychar="
            result += self.keychar
            result += ","

        if result.endswith(","):
            result = result[:len(result)-1]
        return "KeyEvent(" + result + ")"

    ##########
    #   Properties    
    @property
    def event_type(self) -> KeyEventType:
        """ The key event type, never None. """
        return self.__event_type

    @property
    def keycode(self) -> VirtualKey:
        """ The virtual key code, None if not known. """
        return self.__keycode

    @property
    def keychar(self) -> Optional[str]:
        """ The key character, None if not known. """
        return self.__keychar


KeyListener: TypeAlias = Callable[[KeyEvent], None]
""" A signature of a listener to key events - a function
    or a bound method. """

