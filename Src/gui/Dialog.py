"""
    Dialog definition facilities.
"""

import abc
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

class Dialog(abc.ABC):
    """ A common base class for all dialogs. """
    
    ##########
    #   Construction
    def __init__(self, parent: ttk.Widget | None, title: str):
        super().__init__()
        
        self.__parent = None if parent is None else parent.winfo_toplevel()
        self.__root = tk.Toplevel(self.__parent, borderwidth = 4)
        self.__root.title(title)

    ##########
    #   Properties    
    @property
    def parent(self) -> ttk.Widget | None:
        """ Returns the parent top-level widget of this Dialog. """
        return self.__parent
    
    @property
    def root(self) -> tk.Toplevel:
        """ Returns the root pane of this dialog. """
        return self.__root

    ##########
    #   Operations
    def center_in_parent(self) -> None:
        if self.parent is None:
            self.center_in_screen()
        else:
            w = self.__root.winfo_width()
            h = self.__root.winfo_height()
            pw = self.__parent.winfo_width()
            ph = self.__parent.winfo_height()
            px = self.__parent.winfo_x()
            py = self.__parent.winfo_y()
            x = px + (pw/2) - (w/2)
            y = py + (ph/2) - (h/2)
            self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def center_in_screen(self) -> None:
        w = self.__root.winfo_width()
        h = self.__root.winfo_height()
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        x = (sw/2) - (w/2)
        y = (sh/2) - (h/2)
        self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def do_modal(self):
        self.__parent.wait_window(self.__root)

    ##########
    #   Implementation    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass
