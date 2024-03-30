"""
    Defines the common base for all Admin skin actions.
"""
from typing import Optional

from awt.Action import Action
from awt.KeyStroke import KeyStroke

from gui.skins.admin.MainFrame import MainFrame # TODO Acions are for all skins!

class ActionBase(Action):
    """ The common base class for all "admin" skin actions. """

    ##########
    #   Construction
    def __init__(self,
                 main_frame: MainFrame,
                 name: str,
                 description: Optional[str] = None,
                 shortcut: Optional[KeyStroke] = None):
        Action.__init__(self, name=name, description=description, shortcut=shortcut)
        assert isinstance(main_frame, MainFrame)

        self.__main_frame = main_frame

    ##########
    #   Properties
    @property
    def main_frame(self) -> "MainFrame":
        """ The MainFrame to which this Action is bound; never None. """
        return self.__main_frame
