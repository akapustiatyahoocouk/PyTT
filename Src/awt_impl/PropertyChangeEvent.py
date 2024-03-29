from typing import final, Optional, TypeAlias, Callable, Any
from enum import Enum
import tkinter as tk

import awt_impl.Event

class PropertyChangeEvent(awt_impl.Event.Event):
    """ A "property change" event - signals that an observable
        property of some object has changed. """

    ##########
    #   Construction
    def __init__(self, source, affected_object: Any, changed_property: str):
        """ Constructs the event. """
        super().__init__(source)
        
        assert affected_object is not None
        assert isinstance(changed_property, str)
        
        self.__affected_object = affected_object
        self.__changed_property = changed_property

    ##########
    #   object
    def __str__(self) -> str:
        result = ""
        if self.source is not None:
            result += "source="
            result += str(self.source)
        return ("PropertyChangeEvent(" + result + "," +
                repr(self.__affected_object) + "," +
                self.__changed_property + ")")

PropertyChangeListener: TypeAlias = Callable[[PropertyChangeEvent,Any,str], None]
""" A signature of a listener to property change events - a function
    or a bound method. """
