"""
    The set of actions defined by Admin skin.
"""
#   Python standard library
from typing import final

#   Internal dependencies on modules within the same component
from gui.implementation.actions.ExitAction import ExitAction
from gui.implementation.actions.AboutAction import AboutAction

##########
#   Public entities
@final
class ActionSet:
    """ The set of all Actions provided by the Admin skin. """

    ##########
    #   Construction
    def __init__(self):
        self.__exit = ExitAction()
        self.__about = AboutAction()

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
