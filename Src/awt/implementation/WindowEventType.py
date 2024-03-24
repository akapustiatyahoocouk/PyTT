""" The type of a window event. """

#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class WindowEventType(Enum):
    """ The type of a window event. """

    ##########
    #   Constants
    WINDOW_MINIMIZED = 1
    """ A window was minimized. """

    WINDOW_MAXIMIZED = 2
    """ A window was maximized. """

    WINDOW_RESTORED = 3
    """ A window was restored to normal state after
        having been minimized or maximized. """

    WINDOW_CLOSING = 4
    """ The user attempts to close the window. """
