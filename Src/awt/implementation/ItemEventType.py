""" The item event types. """
#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class ItemEventType(Enum):
    """ The type of an item event. """

    ##########
    #   Constants
    ITEM_SELECTED = 1
    """ A item was selected. """

    ITEM_UNSELECTED = 2
    """ A item was unselected. """

    ITEM_STATE_CHANGED = 3
    """ An item state has changed. """
