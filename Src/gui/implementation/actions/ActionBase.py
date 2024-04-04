"""
    Defines the common base for all Admin skin actions.
"""
#   Python standard library
from typing import Optional
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component

##########
#   Public entities
class ActionBase(Action):
    """ The common base class for all "admin" skin actions. """

    ##########
    #   Construction
    def __init__(self,
                 name: str,
                 hotkey: Optional[str] = None,
                 description: Optional[str] = None,
                 shortcut: Optional[KeyStroke] = None,
                 small_image: Optional[tk.PhotoImage] = None,
                 large_image: Optional[tk.PhotoImage] = None):
        Action.__init__(self, name=name, hotkey=hotkey, description=description, 
                        shortcut=shortcut, small_image=small_image, large_image=large_image)
        assert isinstance(name, str)
