""" Defines the "Create workspace" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.CreateWorkspaceDialog import CreateWorkspaceDialog, CreateWorkspaceDialogResult
from ..misc.CurrentWorkspace import CurrentWorkspace
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
            new_workspace = dlg.created_workspace
            #   Use the newly created workspace as "current" workspace
            old_workspace = CurrentWorkspace.get()
            CurrentWorkspace.set(new_workspace)
            if old_workspace:
                #   TODO if there is a "current" activity, stop and record it
                try:
                    old_workspace.close()
                except Exception as ex:
                    pass    # TODO show error dialog
        #   Record the newly created workspace as "last used"
        WorkspaceSettings.last_workspace_address = new_workspace.address
