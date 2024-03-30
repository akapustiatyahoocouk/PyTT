"""
    The set of actions defined by Admin skin.
"""
from typing import final

from gui.skins.admin.MainFrame import MainFrame # TODO Acions are for all skins!
from gui.actions.ExitAction import ExitAction
from gui.actions.AboutAction import AboutAction

@final
class ActionSet:
    """ The set of all Actions provided by the Admin skin. """

    ##########
    #   Construction
    def __init__(self, main_frame: MainFrame):
        self.__exit = ExitAction(main_frame)
        self.__about = AboutAction(main_frame)

    ##########
    #   Actions
    @property
    def exit(self) -> ExitAction:
        """ The "Exit PyTT" action. """
        return self.__exit

    @property
    def about(self) -> AboutAction:
        """ The "About PyTT" action. """
        return self.__about
