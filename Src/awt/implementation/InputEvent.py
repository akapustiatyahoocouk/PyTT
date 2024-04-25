""" A generic input event - the user has performed some action from UI. """
#   Python standard library
from typing import Any

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .InputEventModifiers import InputEventModifiers

##########
#   Public entities
class InputEvent(Event):
    """ A generic user input event. """

    ##########
    #   Construction
    def __init__(self, source,
                 modifiers: InputEventModifiers = None):
        """ Constructs the event with the specified source and modifiers. """
        Event.__init__(self, source)

        assert (modifiers is None) or isinstance(modifiers, InputEventModifiers)
        self.__modifiers = InputEventModifiers.NONE if (modifiers is None) else modifiers

    ##########
    #   Properties
    @property
    def modifiers(self: Any):
        """ The modifiers active at the time this event was raised. """
        return self.__modifiers
