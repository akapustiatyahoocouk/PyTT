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
    NORMAL = 1
    MAXIMIZED = 2
    ICONIFIED = 3
    WITHDRAWN = 4

