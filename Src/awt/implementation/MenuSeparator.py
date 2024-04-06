#   Python standard library
from typing import Optional
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .KeyStroke import KeyStroke
from .MenuItem import MenuItem
from .Action import Action
from .ActionEvent import ActionEvent

##########
#   Public entities
class MenuSeparator(MenuItem):

    ##########    
    #   Construction
    def __init__(self):
        MenuItem.__init__(self)
        
    ##########
    #   MenuItem (Properties) TODO raise to MenuItem class ?
    @property
    def label(self) -> str:
        raise NotImplementedError()

    @label.setter
    def label(self, new_label: str) -> None:
        raise NotImplementedError()

    @property
    def hotkey(self) -> str:
        raise NotImplementedError()

    @hotkey.setter
    def hotkey(self, new_hotkey: str) -> None:
        raise NotImplementedError()

    @property
    def shortcut(self) -> str:
        raise NotImplementedError()

    @label.setter
    def shortcut(self, new_shortcut: KeyStroke) -> None:
        raise NotImplementedError()
