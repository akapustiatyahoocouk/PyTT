from typing import final, Optional

import tkinter as tk
import tkinter.ttk as ttk

import resources
import awt_impl.GuiRoot
import awt_impl.BaseWidgetMixin
import awt_impl.BaseWidgetMixin
import awt_impl.MenuBar

@final
class TopFrame(tk.Toplevel,
               awt_impl.BaseWidgetMixin.BaseWidgetMixin):
    """ The generic top-level UI frame. """
    
    def __init__(self):
        tk.Toplevel.__init__(self, awt_impl.GuiRoot.GuiRoot.tk)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
        
        self.__menu_bar = None

        #self.transient(awt_impl.GuiRoot.GuiRoot.tk)
        self.title(awt_impl.GuiRoot.GuiRoot.tk.title())
        self.wm_iconphoto(True, resources.Resources.PRODUCT_ICON)
        self.geometry("600x400")

    ##########
    #   tkinter support
    def tk(self) -> tk.Tk:
        return self.__tk
    
    ##########
    #   Properties
    @property
    def menu_bar(self) -> Optional[awt_impl.MenuBar.MenuBar]:
        return self.__menu_bar

    @menu_bar.setter
    def menu_bar(self, mb: Optional[awt_impl.MenuBar.MenuBar]) -> None:
        if mb is None:
            if self.__menu_bar is not None:
                self.__menu_bar._impl.master = None
            self["menu"] = ""
            self.__menu_bar = None
        else:
            assert isinstance(mb, Optional[awt_impl.MenuBar.MenuBar])
            mb._impl.master._impl = self
            self["menu"] = mb._impl
            self.__menu_bar = mb
