""" Defines the "About PyTT" action. """
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
class AboutAction(ActionBase):
    """ The "About PyTT" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.About")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with AboutDialog(self.dialog_parent) as dlg:
            dlg.do_modal()
