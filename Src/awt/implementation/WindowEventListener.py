""" Defines a signature of a listener to window events - a 
    function or a bound method. """

#   Python standard library
from typing import Callable, TypeAlias

#   Internal dependencies on modules within the same component
from .WindowEvent import WindowEvent

##########
#   Public entities
WindowEventListener: TypeAlias = Callable[[WindowEvent], None]
""" A signature of a listener to window events - a function
    or a bound method. """
