from typing import final

import awt
import dialogs
import admin_skin_impl.MainFrame
import admin_skin_impl.actions.ActionBase

class AboutAction(admin_skin_impl.actions.ActionBase.ActionBase):
    """ The "About PyTT" action. """
    
    ##########
    #   Construction
    def __init__(self, 
                 main_frame: admin_skin_impl.MainFrame.MainFrame):
        admin_skin_impl.actions.ActionBase.ActionBase.__init__(
            self,
            main_frame,
            "A&bout", 
            "Shows PyTT bersion and copyright information",
            awt.KeyStroke(awt.VirtualKey.VK_F1, awt.InputEventModifiers.CONTROL))

    ##########
    #   awt.Action - Operations
    def execute(self, evt: awt.ActionEvent) -> None:
        with dialogs.AboutDialog(self.main_frame) as dlg:
            dlg.do_modal()
