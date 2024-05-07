""" Defines "Manage activity types" action. """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.ManageActivityTypesDialog import *
from .ActionBase import ActionBase

##########
#   Public entities
@final
class ManageActivityTypesAction(ActionBase):
    """ The "Manage activity types" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.ManageActivityTypes")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with ManageActivityTypesDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
