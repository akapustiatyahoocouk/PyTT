""" Defines "Manage public activities" action. """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.ManagePublicActivitiesDialog import *
from .ActionBase import ActionBase

##########
#   Public entities
@final
class ManagePublicActivitiesAction(ActionBase):
    """ The "Manage public activities" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.ManagePublicActivities")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with ManagePublicActivitiesDialog(self.dialog_parent) as dlg:
            dlg.do_modal()

