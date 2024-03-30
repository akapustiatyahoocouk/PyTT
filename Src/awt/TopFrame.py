from typing import final, Optional

import tkinter as tk

from util_api import UtilResources
from awt.GuiRoot import GuiRoot
from awt.BaseWidgetMixin import BaseWidgetMixin
from awt.MenuBar import MenuBar

@final
class TopFrame(tk.Toplevel, BaseWidgetMixin):
    """ The generic top-level UI frame. """
    
    def __init__(self):
        """ Constructs a top-level frame. """
        tk.Toplevel.__init__(self, GuiRoot.tk)
        BaseWidgetMixin.__init__(self)
        
        self.__menu_bar = None

        #self.state("withdrawn")
        #self.transient(awt.GuiRoot.GuiRoot.tk)
        self.title(GuiRoot.tk.title())
        self.wm_iconphoto(True, UtilResources.PRODUCT_ICON_LARGE)
        self.geometry("600x400")

    ##########
    #   tkinter support
    def tk(self) -> tk.Tk:
        return self.__tk
    
    ##########
    #   Properties
    @property
    def menu_bar(self) -> Optional[MenuBar]:
        return self.__menu_bar

    @menu_bar.setter
    def menu_bar(self, mb: Optional[MenuBar]) -> None:
        if mb is self.__menu_bar:
            return#   Already there
        if mb is None:
            if self.__menu_bar is not None:
                self.__menu_bar._Menu__tk_impl.master = None
            self["menu"] = ""
            self.__menu_bar = None
        else:
            assert isinstance(mb, Optional[MenuBar])
            mb._Menu__tk_impl.master._impl = self
            self["menu"] = mb._Menu__tk_impl
            self.__menu_bar = mb
