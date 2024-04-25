"""
    Dialog definition facilities.
"""
#   Python standard library
from tkinter.tix import ComboBox
from typing import Optional
from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .GuiRoot import GuiRoot
from .Button import Button
from .Window import Window
from .WindowEventType import WindowEventType
from .WindowEvent import WindowEvent

##########
#   Public entities
class Dialog(Window):
    """ A common base class for all dialogs. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, title: str):
        Window.__init__(self,
                        parent if parent is not None else GuiRoot.tk,
                        title)

        self.configure(padx=4, pady=4)
        self.__parent = GuiRoot.tk if parent is None else parent.winfo_toplevel()
        self.title(title)
        # TODO keep? kill? self.resizable(False, False)

        self.__ok_button : Button = None
        self.__cancel_button : Button = None

        self.__running_modal = False

        #   Set up event handlers
        self.focusable = False
        self.bind("<Escape>", self.__on_tk_escape)
        self.bind("<Return>", self.__on_tk_return)
        self.add_window_listener(self.__window_listener)

    ##########
    #   object (entry/exit protocol needed for Dialog.do_modal
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.destroy()

    ##########
    #   tk.Wm
    def attributes(self, *args):
        """ TODO document. """
        raise NotImplementedError("Use AWT-defined properties instead")

    ##########
    #   Properties
    @property
    def parent(self) -> ttk.Widget | None:
        """ The parent top-level widget of this Dialog. """
        #   TODO add to TopFrame ?
        return self.__parent

    @property
    def ok_button(self):
        """ The special button of this dialog that gets "clicked"
            when the user presses ENTER within the dialog. """
        return self.__ok_button

    @ok_button.setter
    def ok_button(self, button: Button):
        """ Sets the special button of this dialog that gets "clicked"
            when the user presses ENTER within the dialog. """
        assert (button is None) or isinstance(button, Button)

        #   TODO make sure the "button" is a child widget of this Dialog
        if button is self.__ok_button:
            return  #   Nothing to do
        if self.__ok_button is not None:
            self.__ok_button.configure(default="normal")
        self.__ok_button = button
        if self.__ok_button is not None:
            self.__ok_button.configure(default="active")

    @property
    def cancel_button(self):
        """ The special button of this dialog that gets "clicked"
            when the user presses ESC within the dialog or closes
            the dialog via the window manager GUI. """
        return self.__cancelLDi_button

    @ok_button.setter
    def cancel_button(self, button: Button):
        """ Sets the special button of this dialog that gets "clicked"
            when the user presses ESC within the dialog or closes
            the dialog via the window manager GUI. """
        assert (button is None) or isinstance(button, Button)
        #   TODO make sure the "button" is a child widget of this Dialog
        self.__cancel_button = button

    ##########
    #   Operations
    def do_modal(self) -> None:
        """
            Runs this dialog as a modal dialog, returning only when
            the user closes the dialog by whatever means are allowed.
        """
        assert not self.__running_modal

        if self.__parent is GuiRoot.tk:
            GuiRoot.tk.deiconify()

        #self.wait_visibility()
        self.center_in_parent()
        self.grab_set()
        self.transient(self.__parent)

        self.__running_modal = True
        self.initial_focus.focus_force()

        self.__parent.wait_window(self)

        self.grab_release()

        if self.__parent is GuiRoot.tk:
            GuiRoot.tk.withdraw()

    def end_modal(self):
        assert self.__running_modal
        self.__running_modal = False
        self.destroy()

    @property
    def initial_focus(self) -> tk.BaseWidget:
        """ The dialog widget which gets the focus when Dialog
            is shown; default is first visible focusable enabled
            widget of the dialog. """
        ff = Dialog.__find_first_focusable_widget(self)
        return ff if ff is not None else self

    ##########
    #   Implementation
    @staticmethod
    def __find_first_focusable_widget(parent: tk.BaseWidget)  -> tk.BaseWidget:
        if parent.visible and parent.enabled and parent.focusable:
            return parent
        for child in parent.winfo_children():
            ff = Dialog.__find_first_focusable_widget(child)
            if ff is not None:
                return ff
        return None

    ##########
    #   Tk event handlers
    def __on_tk_escape(self, *args):
        if ((self.__cancel_button is not None) and self.__cancel_button.winfo_exists() and
             self.__cancel_button.showing and self.__cancel_button.enabled):
            self.__cancel_button.invoke()
        return "break"

    def __on_tk_return(self, *args):
        if ((self.__ok_button is not None) and self.__ok_button.winfo_exists() and
             self.__ok_button.showing and self.__ok_button.enabled):
            self.__ok_button.invoke()
        return "break"

    ##########
    #   Event listeners
    def __window_listener(self, evt: WindowEvent):
        if evt.event_type is WindowEventType.WINDOW_CLOSING:
            evt.processed = True
            self.__on_tk_escape()
