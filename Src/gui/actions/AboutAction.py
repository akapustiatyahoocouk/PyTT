"""
    Defines the "About PyTT" admin skin action.
"""
#   Python standard library
from typing import final

from awt.KeyStroke import KeyStroke
from awt.VirtualKey import VirtualKey
from awt.InputEventModifiers import InputEventModifiers
from awt.ActionEvent import ActionEvent

#   Internal dependencies on modules within the same component
from gui.dialogs.AboutDialog import AboutDialog
from gui.skins.admin.MainFrame import MainFrame
from gui.actions.ActionBase import ActionBase
from gui.GuiResources import GuiResources

@final
class AboutAction(ActionBase):
    """ The "About PyTT" action. """

    ##########
    #   Construction
    def __init__(self, main_frame: MainFrame):
        ActionBase.__init__(self,
                            main_frame,
                            name=GuiResources.ACTIONS_ABOUT_NAME, 
                            hotkey=GuiResources.ACTIONS_ABOUT_HOTKEY,
                            description=GuiResources.ACTIONS_ABOUT_DESCRIPTION,
                            shortcut=KeyStroke(VirtualKey.VK_F1, InputEventModifiers.CONTROL),  # TODO from from GuiResources
                            small_image=GuiResources.ACTIONS_ABOUT_SMALL_IMAGE,
                            large_image=GuiResources.ACTIONS_ABOUT_LARGE_IMAGE)

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        with AboutDialog(self.main_frame) as dlg:
            dlg.do_modal()
