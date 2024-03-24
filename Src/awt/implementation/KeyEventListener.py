""" Defines the "key event listener" ADT - a function that
    is notified when KeyEvent occurs. """
#   Python standard library
from typing import TypeAlias, Callable

#   Internal dependencies on modules within the same component
from .KeyEvent import KeyEvent

##########
#   Public entities
KeyEventListener: TypeAlias = Callable[[KeyEvent], None]
""" A signature of a listener to key events - a function
    or a bound method. """
