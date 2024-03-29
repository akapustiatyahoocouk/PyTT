"""
    Defines the "About PyTT" admin skin action.
"""
from typing import final

from awt import KeyStroke, VirtualKey, InputEventModifiers, ActionEvent
from dialogs import AboutDialog
from admin_skin_impl.MainFrame import MainFrame
from admin_skin_impl.actions.ActionBase import ActionBase

@final
class AboutAction(ActionBase):
    """ The "About PyTT" action. """

    ##########
    #   Construction
    def __init__(self, main_frame: MainFrame):
        ActionBase.__init__(self,
                            main_frame,
                            "A&bout", 
                            "Shows PyTT bersion and copyright information",
                            KeyStroke(VirtualKey.VK_F1, InputEventModifiers.CONTROL))

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with AboutDialog(self.main_frame) as dlg:
            dlg.do_modal()
