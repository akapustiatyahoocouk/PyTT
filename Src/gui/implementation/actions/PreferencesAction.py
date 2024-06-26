""" Defines "PyTT preferences" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.PreferencesDialog import *
from .ActionBase import ActionBase

##########
#   Public entities
@final
class PreferencesAction(ActionBase):
    """ The "PyTT preferences" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.Preferences")

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with PreferencesDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
