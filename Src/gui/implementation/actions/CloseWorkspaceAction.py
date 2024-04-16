"""
    Defines the "Close workspace" admin skin action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.AboutDialog import AboutDialog
from gui.implementation.actions.ActionBase import ActionBase
from gui.implementation.skins.Skin import Skin
from gui.implementation.skins.ActiveSkin import ActiveSkin
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class CloseWorkspaceAction(ActionBase):
    """ The "Close workspace" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.CloseWorkspace")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        ws = Workspace.current
        Workspace.current = None
        if ws is not None:
            #   TODO if there is a "current" activity, stop and record it
            try:
                ws.close()
            except Exception as ex:
                pass    # TODO show error dialog
