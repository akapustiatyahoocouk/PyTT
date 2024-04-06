#   Python standard library
from typing import Callable
from inspect import signature
import tkinter as tk

#   Internal dependencies on modules within the same component
from .KeyEvent import KeyEvent, KeyEventType
from .KeyEventProcessorMixin import KeyEventProcessorMixin

##########
#   Public entities
class BaseWidgetMixin(KeyEventProcessorMixin):
    """ A mix-in class that adds functionality to BaseWidgets. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        KeyEventProcessorMixin.__init__(self)

        self.__visible = True
        self.__focusable = True
        self.configure(takefocus=1)
        
        self.bind("<KeyPress>", self.__on_tk_keydown)
        self.bind("<KeyRelease>", self.__on_tk_keyup)

    ##########
    #   Properties
    @property
    def visible(self):
        """ True if this widget is visible, False if hidden. """
        return self.__visible

    @visible.setter
    def visible(self, new_visible: bool):
        """
            Shows or hides this widget.

            @param new_visible:
                True to show this widget, false to hide.
        """
        assert isinstance(new_visible, bool)
        if new_visible != self.__visible:
            self.__visible = new_visible
            if new_visible:
                self.pack()
            else:
                self.pack_forget()

    @property
    def enabled(self):
        """ True if this widget is enabled, False if disabled. """
        return tk.DISABLED not in self.state()

    @enabled.setter
    def enabled(self, yes: bool):
        """
            Enables or disables this widget.

            @param value:
                True to enable this widget, false to disable.
        """
        if yes:
            self.state(["!disabled"])
        else:
            self.state(["disabled"])

    @property
    def focusable(self) -> bool:
        return self.__focusable

    @focusable.setter
    def focusable(self, new_focusable: bool) -> None:
        assert isinstance(new_focusable, bool)
        if new_focusable != self.__focusable:
            self.__focusable = new_focusable
            self.configure(takefocus=1 if new_focusable else 0)
    
    ##########
    #   Operations
    def center_in_parent(self) -> None:
        """ TODO document. """
        if isinstance(self.parent, tk.Tk):
            self.center_in_screen()
        else:
            w = self.winfo_width()
            h = self.winfo_height()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            px = self.parent.winfo_x()
            py = self.parent.winfo_y()
            x = px + int(pw/2) - int(w/2)
            y = py + int(ph/2) - int(h/2)
            #   TODO Try to keep the dialog within screen boundaries
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def center_in_screen(self) -> None:
        """ TODO document. """
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int(sw/2) - int(w/2)
        y = int(sh/2) - int(h/2)
        #   TODO Try to keep the dialog within screen boundaries
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    ##########
    #   Tk event handlers
    def __on_tk_keydown(self, evt: tk.Event):
        #print(evt)
        ke = KeyEvent(self, KeyEventType.KEY_DOWN, evt)
        self.process_key_event(ke)
        if ke.keychar is not None:
            ce = KeyEvent(self, KeyEventType.KEY_CHAR, evt)
            self.process_key_event(ce)

    def __on_tk_keyup(self, evt: tk.Event):
        #print(evt)
        ke = KeyEvent(self, KeyEventType.KEY_UP, evt)
        self.process_key_event(ke)
