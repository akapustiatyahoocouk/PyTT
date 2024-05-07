""" Defines "Manage users" action. """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.ManageUsersDialog import *
from .ActionBase import ActionBase

##########
#   Public entities
@final
class ManageUsersAction(ActionBase):
    """ The "Manage users" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.ManageUsers")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with ManageUsersDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
