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
    MINIMIZE = 1
    """ A window was minimized. """

    MAXIMIZE = 2
    """ A window was maximized. """

    RESTORE = 3
    """ A window was restored to normal state after 
        having been minimized or maximized. """

    CLOSING = 4
    """ The user attempts to close the window. """
