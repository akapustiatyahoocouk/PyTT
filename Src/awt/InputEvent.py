#   Python standard library
from abc import ABCMeta
from typing import Any

#   Internal dependencies on modules within the same component
from awt.Event import Event
from awt.InputEventModifiers import InputEventModifiers

class InputEvent(Event):
    """ A generic user input event. """

    ##########
    #   Construction
    def __init__(self, source, 
                 modifiers: InputEventModifiers = None):
        """ Constructs the event with the specified source and modifiers. """
        super().__init__(source)
        
        assert (modifiers is None) or isinstance(modifiers, InputEventModifiers)
        self.__modifiers = InputEventModifiers.NONE if (modifiers is None) else modifiers

    ##########
    #   Properties
    @property
    def modifiers(self: Any):
        """ The modifiers active at the time this event was raised. """
        return self.__modifiers
