""" The type of a widget event. """

#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class WidgetEventType(Enum):
    """ The type of a widget event. """

    ##########
    #   Constants
    WIDGET_SHOWN = 1
    """ The widget has been resized. """

    WIDGET_HIDDEN = 2
    """ The widget has been hidden. """

    WIDGET_MOVED = 3
    """ The widget has been moved. """

    WIDGET_RESIZED = 4
    """ The widget has been resized. """
