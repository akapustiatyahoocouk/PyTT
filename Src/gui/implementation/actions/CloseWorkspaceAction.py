""" Defines the "Close workspace" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.AboutDialog import AboutDialog
from ..actions.ActionBase import ActionBase
from ..skins.Skin import Skin
from ..skins.ActiveSkin import ActiveSkin
from ..misc.CurrentWorkspace import CurrentWorkspace
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
        ws = CurrentWorkspace.get()
        CurrentWorkspace.set(None)
        if ws is not None:
            #   TODO if there is a "current" activity, stop and record it
            try:
                ws.close()
            except Exception as ex:
                pass    # TODO show error dialog
