#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class KeyEventType(Enum):
    """ The key event type. """

    ##########
    #   Constants
    KEY_DOWN = 1
    """ A key was pressed. """

    KEY_UP = 2
    """ A key was released. """

    KEY_CHAR = 3
    """ A key was pressed that represents a typed character;
        always occurs between KEY_DOWN and KEY_UP key events. """

