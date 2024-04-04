"""
    Defines the common base for all Admin skin actions.
"""
#   Python standard library
from typing import Optional
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.skins.ActiveSkin import ActiveSkin

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
        
    ##########
    #   Properties
    @property
    def dialog_parent(self) -> tk.BaseWidget:
        active_skin = ActiveSkin.get()
        return active_skin.dialog_parent if active_skin is not None else GuiRoot.tk
