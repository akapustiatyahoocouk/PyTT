"""
    Defnes "exit PyTT" admin skin action.
"""
from typing import final

from awt.KeyStroke import KeyStroke
from awt.VirtualKey import VirtualKey
from awt.InputEventModifiers import InputEventModifiers
from awt.ActionEvent import ActionEvent

from gui.skins.admin.MainFrame import MainFrame # TODO actions are for ALL skins!
from gui.actions.ActionBase import ActionBase
from gui.GuiResources import GuiResources

@final
class ExitAction(ActionBase):
    """ The "Exit PyTT" action. """

    ##########
    #   Construction
    def __init__(self, main_frame: MainFrame):
        ActionBase.__init__(self,
                            main_frame,
                            name=GuiResources.ACTIONS_EXIT_NAME, 
                            hotkey=GuiResources.ACTIONS_EXIT_HOTKEY,
                            description=GuiResources.ACTIONS_EXIT_DESCRIPTION,
                            shortcut=KeyStroke(VirtualKey.VK_F4, InputEventModifiers.ALT),  # TODO from from GuiResources
                            small_image=GuiResources.ACTIONS_EXIT_SMALL_IMAGE,
                            large_image=GuiResources.ACTIONS_EXIT_LARGE_IMAGE)

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        self.main_frame.destroy()
