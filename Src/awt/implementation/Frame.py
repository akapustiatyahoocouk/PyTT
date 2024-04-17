#   Python standard library
from typing import final, Optional
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Window import Window
from .GuiRoot import GuiRoot

##########
#   Public entities
class Frame(Window):
    """ The generic top-level UI frame. """

    def __init__(self, title: str = GuiRoot.tk.title()):
        """ Constructs a top-level frame. """
        Window.__init__(self, parent=GuiRoot.tk, title=title)

        #TODO kill off self.state("withdrawn")
        #TODO kill off self.transient(awt.GuiRoot.GuiRoot.tk)
        #TODO kill off self.title(GuiRoot.tk.title())
        #TODO kill off self.wm_iconphoto(True, UtilResources.image("PyTT.LargeImage"))
        #TODO kill off self.geometry("600x400")
