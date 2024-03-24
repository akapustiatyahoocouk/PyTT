""" Defines the ActionEventListener ADT. """
#   Python standard library
from typing import TypeAlias, Callable

#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent

ActionEventListener: TypeAlias = Callable[[ActionEvent], None]
""" A signature of a listener to action events - a function
    or a bound method. """
