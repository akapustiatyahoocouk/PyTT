from typing import final, Optional
from enum import Enum
import tkinter as tk

import awt_impl.InputEvent
import awt_impl.VirtualKey

@final
class KeyEventType(Enum):
    """ The key event type. """

    ##########
    #   Constants
    KEY_DOWN = 1
    """ A key was pressed. """

    KEY_UP = 2
    """ A key was released. """

    KEY_CHAR = 3
    """ A key was pressed that represents a typed character;
        always occurs between KEY_DOWN and KEY_UP key events. """

class KeyEvent(awt_impl.InputEvent.InputEvent):
    """ A key input event. """

    ##########
    #   Construction
    def __init__(self, source, event_type: KeyEventType, tk_evt: tk.Event):
        """ Constructs the event from the specified tk key event. """
        super().__init__(source, tk_evt.state)
        
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
            
        self.__keycode = awt_impl.VirtualKey.VirtualKey.from_tk_string(tk_evt.keysym)

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

        if len(self.modifiers_string) > 0:
            result += "modifiers="
            result += self.modifiers_string
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
    def keycode(self) -> awt_impl.VirtualKey.VirtualKey:
        """ The virtual key code, None if not known. """
        return self.__keycode

    @property
    def keychar(self) -> Optional[str]:
        """ The key character, None if not known. """
        return self.__keychar

