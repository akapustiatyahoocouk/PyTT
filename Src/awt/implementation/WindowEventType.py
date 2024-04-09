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
    MINIMIZED = 1
    """ A window was minimized. """

    MAXIMIZED = 2
    """ A window war maximized. """

    RESTORED = 3
    """ window was restored to normal state after having been
        minimized or maximized. """

    CLOSING = 4
    """ The user attempts to close the window. """
