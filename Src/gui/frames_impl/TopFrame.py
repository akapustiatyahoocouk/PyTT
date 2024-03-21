from typing import final

import tkinter as tk
import tkinter.ttk as ttk

import util.resources as utilres
from gui.root import GuiRoot
import gui.events as events

@final
class TopFrame(tk.Toplevel, events.EventProcessor):
    """ The generic top-level UI frame. """
    
    def __init__(self):
        tk.Toplevel.__init__(self, GuiRoot.tk)
        events.EventProcessor.__init__(self)
        
        self.transient(GuiRoot.tk)
        self.title(GuiRoot.tk.title())
        self.wm_iconphoto(True, utilres.UtilResources.PRODUCT_ICON)
        self.geometry('600x400')

    ##########
    #   tkinter support    
    def tk(self) -> tk.Tk:
        return self.__tk