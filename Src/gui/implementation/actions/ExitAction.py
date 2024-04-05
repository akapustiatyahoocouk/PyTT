"""
    Defnes "exit PyTT" admin skin action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.actions.ActionBase import ActionBase
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class ExitAction(ActionBase):
    """ The "Exit PyTT" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.Exit")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        GuiRoot.tk.quit()
