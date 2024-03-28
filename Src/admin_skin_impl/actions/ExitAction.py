from typing import final

import awt
import admin_skin_impl.MainFrame
import admin_skin_impl.actions.ActionBase

class ExitAction(admin_skin_impl.actions.ActionBase.ActionBase):
    """ The "Exit PyTT" action. """
    
    ##########
    #   Construction
    def __init__(self, 
                 main_frame: admin_skin_impl.MainFrame.MainFrame):
        admin_skin_impl.actions.ActionBase.ActionBase.__init__(
            self,
            main_frame,
            "E&xit", 
            "Exits PyTT",
            awt.KeyStroke(awt.VirtualKey.VK_F4, awt.InputEventModifiers.ALT))

    ##########
    #   awt.Action - Operations
    def execute(self, evt: awt.ActionEvent) -> None:
        self.main_frame.destroy()
