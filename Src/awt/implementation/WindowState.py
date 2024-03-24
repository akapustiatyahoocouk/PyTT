""" The state of a top-level window (frame, dialog, etc.) """

#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class WindowState(Enum):
    """ The state of a top-level window (frame, dialog, etc.) """

    ##########
    #   Constants
    UNDEFINED = 0
    """ The window state could not be determined. """

    NORMAL = 1
    """ The window is neither minimized nor maximized. """

    MAXIMIZED = 2
    """ The window is maximized. """

    ICONIFIED = 3
    """ The window is minimized. """

    WITHDRAWN = 4
    """ The window is hidden. """
