""" Defines the "item event listener" ADT - a function that
    is notified when ItemEvent occurs. """
#   Python standard library
from typing import TypeAlias, Callable

#   Internal dependencies on modules within the same component
from .ItemEvent import ItemEvent

##########
#   Public entities
ItemEventListener: TypeAlias = Callable[[ItemEvent], None]
""" A signature of a listener to item events - a function
    or a bound method. """
