""" Defines the "Login as a different user" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.LoginDialog import *
from .ActionBase import ActionBase
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials

##########
#   Public entities
@final
class LoginAsDifferentUserAction(ActionBase):
    """ The "Login as a different user" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.LoginAsDifferentUser")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        while True:
            with LoginDialog(self.dialog_parent) as dlg:
                dlg.do_modal()
                if dlg.result is not LoginDialogResult.OK:
                    return
                new_credentials = dlg.credentials
                #   Will the new credentials still grant access to cur "current" workspace?
                try:
                    if CurrentWorkspace.get() is not None:
                        if CurrentWorkspace.get().get_capabilities(new_credentials) == Capabilities.NONE:
                            if MessageBox.show(self.dialog_parent, 
                                               GuiResources.string("ReloginFailedDialog.Title"),
                                               GuiResources.string("ReloginFailedDialog.Prompt",
                                                                   CurrentWorkspace.get().address.display_form),
                                               MessageBoxIcon.QUESTION,
                                               MessageBoxButtons.YES_NO) == MessageBoxResult.YES:
                                continue
                            return  #   without setting new credentials
                    CurrentCredentials.set(new_credentials)
                    return
                except Exception as ex:
                    ErrorDialog.show(self.dialog_parent, ex)
                    return
