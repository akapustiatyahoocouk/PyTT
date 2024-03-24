""" Defines a signature of a listener to widget events - a 
    function or a bound method. """

#   Python standard library
from typing import Callable, TypeAlias

#   Internal dependencies on modules within the same component
from .WidgetEvent import WidgetEvent

WidgetEventListener: TypeAlias = Callable[[WidgetEvent], None]
""" A signature of a listener to widget events - a function
    or a bound method. """
