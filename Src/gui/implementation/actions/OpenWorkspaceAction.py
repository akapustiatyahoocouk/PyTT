""" Defines the "Open workspace" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.implementation.dialogs.OpenWorkspaceDialog import OpenWorkspaceDialog, OpenWorkspaceDialogResult
from gui.implementation.misc.CurrentCredentials import CurrentCredentials
from gui.implementation.misc.CurrentWorkspace import CurrentWorkspace
from gui.resources.GuiResources import GuiResources
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
            new_workspace = dlg.opened_workspace

        #   Make sure "current" credentials grant access
        try:
            new_workspace.login(credentials=CurrentCredentials.get())
        except WorkspaceAccessDeniedError as ex:
            title = GuiResources.string("CannotAccessWorkspaceDialog.Title")
            message = GuiResources.string("CannotAccessWorkspaceDialog.Message",
                                          new_workspace.address.display_form)
            if MessageBox.show(self.dialog_parent, 
                               title,
                               message,
                               MessageBoxIcon.QUESTION,
                               MessageBoxButtons.YES_NO) == MessageBoxResult.YES:
                #   TODO implement re-login!
                return
            new_workspace.close()
            return
        except Exception as ex:
            new_workspace.close()
            ErrorDialog.show(None, ex)
            return
        #   Use the newly created workspace as "current" workspace
        old_workspace = CurrentWorkspace.get()
        CurrentWorkspace.set(new_workspace)
        if old_workspace:
            #   TODO if there is a "current" activity, stop and record it
            try:
                old_workspace.close()
            except Exception as ex:
                ErrorDialog.show(None, ex)
        #   Record the newly created workspace as "last used"
        WorkspaceSettings.last_workspace_address = new_workspace.address
        #   TODO and add it to MRU workspaces list
