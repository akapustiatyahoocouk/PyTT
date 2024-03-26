from typing import final

import tkinter as tk
import tkinter.ttk as ttk

import resources
import awt_impl.GuiRoot
import awt_impl.BaseWidgetMixin
import awt_impl.BaseWidgetMixin

@final
class TopFrame(tk.Toplevel,
               awt_impl.BaseWidgetMixin.BaseWidgetMixin):
    """ The generic top-level UI frame. """
    
    def __init__(self):
        tk.Toplevel.__init__(self, awt_impl.GuiRoot.GuiRoot.tk)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
        
        #self.transient(awt_impl.GuiRoot.GuiRoot.tk)
        self.title(awt_impl.GuiRoot.GuiRoot.tk.title())
        self.wm_iconphoto(True, resources.Resources.PRODUCT_ICON)
        self.geometry("600x400")

    ##########
    #   tkinter support
    def tk(self) -> tk.Tk:
        return self.__tk