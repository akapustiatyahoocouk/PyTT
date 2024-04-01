from typing import final
from enum import Enum

@final
class ResourceType(Enum):
    NONE = 0
    """ The resource does not exist OR its type cannot be determined. """
    
    STRING = 1
    """ The resource is a string (str). """

    IMAGE = 2
    """ The resource is an image (tk.PhotoImage). """
    
    #   TODO keystroke, etc.
