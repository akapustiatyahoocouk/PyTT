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
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class ActionBase(ResourceAwareAction):
    """ The common base class for all "admin" skin actions. """

    ##########
    #   Construction
    def __init__(self,
                 resource_key_base: str):
        ResourceAwareAction.__init__(self, 
                                     resource_factory=GuiResources.factory,
                                     locale_provider=DefaultLocaleProvider.instance,
                                     resource_key_base=resource_key_base)
        
    ##########
    #   Properties
    @property
    def dialog_parent(self) -> tk.BaseWidget:
        active_skin = ActiveSkin.get()
        return active_skin.dialog_parent if active_skin is not None else GuiRoot.tk
