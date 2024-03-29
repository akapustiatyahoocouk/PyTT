from typing import final, Optional

import tkinter as tk

from util import UtilResources
from awt_impl.GuiRoot import GuiRoot
from awt_impl.BaseWidgetMixin import BaseWidgetMixin
from awt_impl.MenuBar import MenuBar

@final
class TopFrame(tk.Toplevel, BaseWidgetMixin):
    """ The generic top-level UI frame. """
    
    def __init__(self):
        tk.Toplevel.__init__(self, GuiRoot.tk)
        BaseWidgetMixin.__init__(self)
        
        self.__menu_bar = None

        #self.transient(awt_impl.GuiRoot.GuiRoot.tk)
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
        if mb is None:
            if self.__menu_bar is not None:
                self.__menu_bar._Menu__impl.master = None
            self["menu"] = ""
            self.__menu_bar = None
        else:
            assert isinstance(mb, Optional[MenuBar])
            mb._Menu__impl.master._impl = self
            self["menu"] = mb._Menu__impl
            self.__menu_bar = mb
