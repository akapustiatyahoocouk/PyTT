import tkinter as tk

import awt_impl.MenuItem
import awt_impl.Menu

class Submenu(awt_impl.MenuItem.MenuItem, awt_impl.Menu.Menu):

    ##########
    #   Construction
    def __init__(self, label: str):
        awt_impl.MenuItem.MenuItem.__init__(self)
        awt_impl.Menu.Menu.__init__(self)

        assert isinstance(label, str)
        self.__label = label
    
    ##########
    #   MenuItem (Properties)
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, lab: str) -> None:
        assert isinstance(label, str)
        self.__label = label
    