from typing import Optional
from abc import ABC

import awt_impl.KeyStroke

class Action(ABC):
    """ A generic "action" is an agent that encapsulates properties 
        of an activity that can be triggered by the user. """
        
    ##########
    #   Construction
    def __init__(self, 
                 name: str, 
                 description: Optional[str] = None, 
                 shortcut: Optional[awt_impl.KeyStroke.KeyStroke] = None) -> None:
        """
            Constructs the action.
            
            @param name:
                The short user-readable name of the action.
            @param description:
                The 1-line user-readable description of the action (optional).
            @param shortcut:
                The keyboard shortcut of the action (optional).
        """
        assert isinstance(name, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, awt_impl.KeyStroke.KeyStroke)

        self.__name = name
        self.__description = description
        self.__shortcut = shortcut
