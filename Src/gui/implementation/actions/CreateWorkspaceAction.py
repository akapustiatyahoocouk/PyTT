"""
    Defines the "Create workspace" admin skin action.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.CreateWorkspaceDialog import CreateWorkspaceDialog, CreateWorkspaceDialogResult
from .ActionBase import ActionBase

##########
#   Public entities
@final
class CreateWorkspaceAction(ActionBase):
    """ The "Create workspace" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.CreateWorkspace")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with CreateWorkspaceDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
            if dlg.result is not CreateWorkspaceDialogResult.OK:
                return
            #   Use the newly created workspace as "current" workspace
            old_workspace = Workspace.current
            Workspace.current = dlg.created_workspace
            if old_workspace:
                try:
                    old_workspace.close()
                except Exception as ex:
                    pass    # TODO show error dialog
        #   Record the newly created workspace as "last used"
        WorkspaceSettings.last_used_workspace_type = Workspace.current.type
        WorkspaceSettings.last_used_workspace_address = Workspace.current.address
