"""
    Defines the "Destroy workspace" admin skin action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.AboutDialog import AboutDialog
from gui.implementation.actions.ActionBase import ActionBase
from gui.implementation.skins.Skin import Skin
from gui.implementation.skins.ActiveSkin import ActiveSkin
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class DestroyWorkspaceAction(ActionBase):
    """ The "Destroy workspace" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.DestroyWorkspace")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        pass
