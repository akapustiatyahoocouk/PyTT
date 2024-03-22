"""
    Dialog definition facilities.
"""
from abc import ABC
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

class Dialog(ABC):
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
            x = px + int(pw/2) - int(w/2)
            y = py + int(ph/2) - int(h/2)
            #   TODO Try to keep the dialog within screen boundaries
            self.__root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def center_in_screen(self) -> None:
        w = self.__root.winfo_width()
        h = self.__root.winfo_height()
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        x = int(sw/2) - int(w/2)
        y = int(sh/2) - int(h/2)
        #   TODO Try to keep the dialog within screen boundaries
        self.__root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        
    def do_modal(self) -> None:
        """
            Runs this dialog as a modal dialog, returning only when
            the user closes the dialog by whatever means are allowed.
        """
        self.__root.wait_visibility()
        self.__root.grab_set()
        self.__root.transient(self.__parent)
        
        self.center_in_parent()
        self.__parent.wait_window(self.__root)

        self.__root.grab_release()
        #self.__root.destroy()

    ##########
    #   Implementation    
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        pass
