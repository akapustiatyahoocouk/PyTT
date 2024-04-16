"""
    Defnes "exit PyTT" admin skin action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ActionBase import ActionBase
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
        #   Close "current" workspace IF there is one
        ws = Workspace.current
        Workspace.current = None
        if ws is not None:
            #   TODO if there is a "current" activity, stop and record it
            ws.close()
        #   We're done - stiop the main loop
        GuiRoot.tk.quit()
