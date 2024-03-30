"""
    Defines the "About PyTT" admin skin action.
"""
from typing import final

from awt.KeyStroke import KeyStroke
from awt.VirtualKey import VirtualKey
from awt.InputEventModifiers import InputEventModifiers
from awt.ActionEvent import ActionEvent
from gui.dialogs.AboutDialog import AboutDialog
from gui.skins.admin.MainFrame import MainFrame
from gui.actions.ActionBase import ActionBase

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
