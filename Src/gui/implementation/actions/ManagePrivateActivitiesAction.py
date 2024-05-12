""" Defines "Manage private activities" action. """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.ManagePrivateActivitiesDialog import *
from .ActionBase import ActionBase

##########
#   Private entities
@final
class ManagePrivateActivitiesAction(ActionBase):
    """ The "Manage private activities" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.ManagePrivateActivities")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with ManagePrivateActivitiesDialog(self.dialog_parent) as dlg:
            dlg.do_modal()


