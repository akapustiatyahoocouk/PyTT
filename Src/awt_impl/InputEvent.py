from abc import ABCMeta
from typing import Any
import re

import awt_impl.Event
import awt_impl.InputEventModifiers

class InputEvent(awt_impl.Event.Event):
    """ A generic user input event. """

    ##########
    #   Construction
    def __init__(self, source, 
                 modifiers: awt_impl.InputEventModifiers = None):
        """ Constructs the event with the specified source and modifiers. """
        super().__init__(source)
        
        assert (modifiers is None) or isinstance(modifiers, awt_impl.InputEventModifiers.InputEventModifiers)
        self.__modifiers = awt_impl.InputEventModifiers.NONE if (modifiers is None) else modifiers

    ##########
    #   Properties
    @property
    def modifiers(self: Any):
        """ The modifiers active at the time this event was raised. """
        return self.__modifiers
