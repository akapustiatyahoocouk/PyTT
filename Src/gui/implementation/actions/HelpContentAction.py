""" Defines the "PyTT Help Content" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.AboutDialog import AboutDialog
from .ActionBase import ActionBase

##########
#   Public entities
@final
class HelpContentAction(ActionBase):
    """ The "PyTT Help Content" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.HelpContent")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with AboutDialog(self.dialog_parent) as dlg:
            dlg.do_modal()

