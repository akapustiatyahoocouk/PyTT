#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class ResourceType(Enum):
    """ The supported resource types. """
    
    NONE = 0
    """ The resource does not exist OR its type cannot be determined. """
    
    STRING = 1
    """ The resource is a string (str). """

    IMAGE = 2
    """ The resource is an image (tk.PhotoImage). """
    
    #   TODO keystroke, etc.
