"""
    Dialog definition facilities.
"""
#   Python standard library
from typing import Optional
from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from awt.BaseWidgetMixin import BaseWidgetMixin
from awt.Button import Button

##########
#   Public entities
class Dialog(tk.Toplevel, BaseWidgetMixin):
    """ A common base class for all dialogs. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, title: str):
        tk.Toplevel.__init__(self,
                             parent if parent is not None else awt.GuiRoot.GuiRoot.tk,
                             padx=4, pady=4)
        BaseWidgetMixin.__init__(self)

        self.__parent = awt.GuiRoot.GuiRoot.tk if parent is None else parent.winfo_toplevel()
        self.title(title)
        # TODO keep? kill? self.resizable(False, False)

        self.__ok_button : Button = None
        self.__cancel_button : Button = None

        self.__running_modal = False

        #   Set up event handlers
        self.bind("<Escape>", self.__on_tk_escape)
        self.bind("<Return>", self.__on_tk_return)

        self.protocol("WM_DELETE_WINDOW", self.__on_tk_escape)

    ##########
    #   object
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.destroy()

    ##########
    #   Properties
    @property
    def parent(self) -> ttk.Widget | None:
        """ Returns the parent top-level widget of this Dialog. """
        #   TODO add to TopFrame ?
        return self.__parent

    @property
    def ok_button(self):
        #   TODO document
        return self.__ok_button

    @ok_button.setter
    def ok_button(self, button: Button):
        #   TODO document
        assert (button is None) or isinstance(button, Button)

        if button is self.__ok_button:
            return  #   Nothing to do
        if self.__ok_button is not None:
            self.__ok_button.configure(default="normal")
        self.__ok_button = button
        if self.__ok_button is not None:
            self.__ok_button.configure(default="active")

    @property
    def cancel_button(self):
        #   TODO document
        return self.__cancelLDi_button

    @ok_button.setter
    def cancel_button(self, button: Button):
        #   TODO document
        assert (button is None) or isinstance(button, Button)
        self.__cancel_button = button

    ##########
    #   Operations
    def do_modal(self) -> None:
        """
            Runs this dialog as a modal dialog, returning only when
            the user closes the dialog by whatever means are allowed.
        """
        assert not self.__running_modal

        self.wait_visibility()
        self.center_in_parent()
        self.grab_set()
        self.transient(self.__parent)

        self.__running_modal = True
        self.__parent.wait_window(self)

        self.grab_release()

    def end_modal(self):
        assert self.__running_modal
        self.__running_modal = False
        self.destroy()

    # TODO kill off
    # def dialog_closing(self) -> bool:
    #     #   TODO document
    #     return True # by default - allow closing the Dialog

    # def dialog_close(self):
    #     #   TODO document
    #     if self.dialog_closing():
    #        #   The default recation is to push the "cancel" button
    #        if ((self.__cancel_button is not None) and self.__cancel_button.enabled):
    #            #   TODO and visible, with all the parents!!!
    #            self.__cancel_button.invoke()

    ##########
    #   Tk event handlers
    def __on_tk_escape(self, *args):
        if ((self.__cancel_button is not None) and self.__cancel_button.winfo_exists() and
            self.__cancel_button.enabled):
            #   TODO and visible, with all the parents!!!
            self.__cancel_button.invoke()

    def __on_tk_return(self, *args):
        if ((self.__ok_button is not None) and self.__ok_button.winfo_exists() and
            self.__ok_button.enabled):
            #   TODO and visible, with all the parents!!!
            self.__ok_button.invoke()
