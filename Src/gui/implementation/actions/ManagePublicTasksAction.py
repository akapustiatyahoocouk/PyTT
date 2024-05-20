""" Defines "Manage public tasks" action. """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.ManagePublicTasksDialog import *
from .ActionBase import ActionBase

##########
#   Public entities
@final
class ManagePublicTasksAction(ActionBase):
    """ The "Manage public tasks" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.ManagePublicTasks")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with ManagePublicTasksDialog(self.dialog_parent) as dlg:
            dlg.do_modal()

