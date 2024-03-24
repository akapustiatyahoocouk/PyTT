#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType

##########
#   Public entities
class View(Panel):
    
    ##########
    #   Construction - from derived classes only
    def __init__(self, parent: tk.BaseWidget) -> None:
        Panel.__init__(self, parent)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        """ The type of this view; MUST be overridden in a derived class. """
        raise NotImplementedError()