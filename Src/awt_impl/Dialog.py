"""
    Dialog definition facilities.
"""
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

import awt

class Dialog(tk.Toplevel):
    """ A common base class for all dialogs. """
    
    ##########
    #   Construction
    def __init__(self, parent: ttk.Widget | None, title: str):
        super().__init__(padx=4, pady=4)
        
        self.__parent = awt.GuiRoot.tk if parent is None else parent.winfo_toplevel()
        self.title(title)
        # TODO keep? kill? self.resizable(False, False)

    ##########
    #   Properties    
    @property
    def parent(self) -> ttk.Widget | None:
        """ Returns the parent top-level widget of this Dialog. """
        return self.__parent
    
    ##########
    #   Operations
    def center_in_parent(self) -> None:
        if isinstance(self.parent, tk.Tk):
            self.center_in_screen()
        else:
            w = self.winfo_width()
            h = self.winfo_height()
            pw = self.__parent.winfo_width()
            ph = self.__parent.winfo_height()
            px = self.__parent.winfo_x()
            py = self.__parent.winfo_y()
            x = px + int(pw/2) - int(w/2)
            y = py + int(ph/2) - int(h/2)
            #   TODO Try to keep the dialog within screen boundaries
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def center_in_screen(self) -> None:
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int(sw/2) - int(w/2)
        y = int(sh/2) - int(h/2)
        #   TODO Try to keep the dialog within screen boundaries
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        
    def do_modal(self) -> None:
        """
            Runs this dialog as a modal dialog, returning only when
            the user closes the dialog by whatever means are allowed.
        """
        self.wait_visibility()
        self.grab_set()
        self.transient(self.__parent)
        
        self.center_in_parent()
        self.__parent.wait_window(self)

        self.grab_release()

    ##########
    #   Implementation    
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        pass
