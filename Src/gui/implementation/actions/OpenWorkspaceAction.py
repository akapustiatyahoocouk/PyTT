"""
    Defines the "Open workspace" action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.OpenWorkspaceDialog import OpenWorkspaceDialog, OpenWorkspaceDialogResult
from .ActionBase import ActionBase

##########
#   Public entities
@final
class OpenWorkspaceAction(ActionBase):
    """ The "Open workspace" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.OpenWorkspace")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with OpenWorkspaceDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
            if dlg.result is not OpenWorkspaceDialogResult.OK:
                return
            #   Use the newly created workspace as "current" workspace
            old_workspace = Workspace.current
            Workspace.current = dlg.opened_workspace
            if old_workspace:
                #   TODO if there is a "current" activity, stop and record it
                try:
                    old_workspace.close()
                except Exception as ex:
                    pass    # TODO show error dialog
            #   Record the newly created workspace as "last used"
        WorkspaceSettings.last_workspace_address = Workspace.current.address
