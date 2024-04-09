#   Python standard library
from typing import Optional, TypeAlias, Callable
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .WindowEventType import WindowEventType

##########
#   Public entities
class WindowEvent(Event):
    """ A window event. """

    ##########
    #   Construction
    def __init__(self, source, event_type: WindowEventType):
        """ Constructs the event. """
        super().__init__(source)
        
        assert ((event_type is WindowEventType.MINIMIZE) or
                (event_type is WindowEventType.MAXIMIZE) or
                (event_type is WindowEventType.RESTORE) or
                (event_type is WindowEventType.CLOSING))
        self.__event_type = event_type

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

        return "WindowEvent(" + result + ")"

    ##########
    #   Properties    
    @property
    def event_type(self) -> WindowEventType:
        """ The window event type, never None. """
        return self.__event_type
