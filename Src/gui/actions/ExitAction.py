"""
    Defnes "exit PyTT" admin skin action.
"""
from typing import final

from awt_api import KeyStroke, VirtualKey, InputEventModifiers, ActionEvent
from gui.skins.admin.MainFrame import MainFrame # TODO actions are for ALL skins!
from gui.actions.ActionBase import ActionBase

@final
class ExitAction(ActionBase):
    """ The "Exit PyTT" action. """

    ##########
    #   Construction
    def __init__(self, main_frame: MainFrame):
        ActionBase.__init__(self,
                            main_frame,
                            "E&xit", 
                            "Exits PyTT",
                            KeyStroke(VirtualKey.VK_F4, InputEventModifiers.ALT))

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        self.main_frame.destroy()
