#   Python standard library
from typing import Optional, TypeAlias, Callable
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .WidgetEventType import WidgetEventType

##########
#   Public entities
class WidgetEvent(Event):
    """ A widget event. """

    ##########
    #   Construction
    def __init__(self, source, event_type: WidgetEventType):
        """ Constructs the event. """
        super().__init__(source)

        assert ((event_type is WidgetEventType.WIDGET_SHOWN) or
                (event_type is WidgetEventType.WIDGET_HIDDEN) or
                (event_type is WidgetEventType.WIDGET_MOVED) or
                (event_type is WidgetEventType.WIDGET_RESIZED))
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

        return "WidgetEvent(" + result + ")"

    ##########
    #   Properties
    @property
    def event_type(self) -> WidgetEventType:
        """ The widget event type, never None. """
        return self.__event_type
