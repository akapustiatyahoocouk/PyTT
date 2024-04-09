#   Python standard library
from typing import Optional, TypeAlias, Callable
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .InputEventModifiers import InputEventModifiers
from .InputEvent import InputEvent
from .ItemEventType import ItemEventType

##########
#   Public entities
class ItemEvent(Event):
    """ An item-related event. """

    ##########
    #   Construction
    def __init__(self, source, event_type: ItemEventType):
        """ Constructs the event. """
        super().__init__(source)

        assert ((event_type is ItemEventType.ITEM_SELECTED) or
                (event_type is ItemEventType.ITEM_UNSELECTED) or
                (event_type is ItemEventType.ITEM_STATE_CHANGED))
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

        return "ItemEvent(" + result + ")"

    ##########
    #   Properties
    @property
    def event_type(self) -> ItemEventType:
        """ The item event type, never None. """
        return self.__event_type
