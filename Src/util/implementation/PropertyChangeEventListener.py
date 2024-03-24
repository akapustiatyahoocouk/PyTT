#   Python standard library
from typing import final, Optional, Callable, Any, TypeAlias
from enum import Enum

#   Internal dependencies on modules within the same component
from .PropertyChangeEvent import PropertyChangeEvent

##########
#   Public entities
PropertyChangeEventListener: TypeAlias = Callable[[PropertyChangeEvent], None]
""" A signature of a listener to property change events - a function
    or a bound method. """
