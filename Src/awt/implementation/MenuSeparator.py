""" The menu separator, useful to assemble menu items into groups. """
#   Python standard library
from typing import Optional

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .KeyStroke import KeyStroke
from .MenuItem import MenuItem

##########
#   Public entities
class MenuSeparator(MenuItem):
    """ The menu separator, useful to assemble menu items into groups. """

    ##########
    #   Construction
    def __init__(self):
        MenuItem.__init__(self)

    ##########
    #   MenuItem (Properties) TODO raise to MenuItem class ?
    @property
    def label(self) -> str:
        """ The textual label of this menu separator; DO NOT USE! """
        raise NotImplementedError()

    @label.setter
    def label(self, new_label: str) -> None:
        """ Sets the textual label of this menu separator; DO NOT USE! """
        raise NotImplementedError()

    @property
    def hotkey(self) -> str:
        """ The character to be used as a keyboard hotkey
            for this menu item; DO NOT USE! """
        raise NotImplementedError()

    @hotkey.setter
    def hotkey(self, new_hotkey: str) -> None:
        """ Sets the character to be used as a keyboard hotkey
            for this menu item; DO NOT USE! """
        raise NotImplementedError()

    @property
    def shortcut(self) -> Optional[KeyStroke]:
        """ The keystroke to be used as a keyboard shortcut
            for this menu item; DO NOT USE! """
        raise NotImplementedError()

    @shortcut.setter
    def shortcut(self, new_shortcut: Optional[KeyStroke]) -> None:
        """ Sets the keystroke to be used as a keyboard shortcut
            for this menu item; DO NOT USE! """
        raise NotImplementedError()
