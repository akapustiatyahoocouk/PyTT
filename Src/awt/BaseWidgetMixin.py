#   Python standard library
from typing import Callable
from inspect import signature
import tkinter as tk

from awt.KeyEvent import KeyEvent, KeyEventType
from awt.KeyEventProcessorMixin import KeyEventProcessorMixin

class BaseWidgetMixin(KeyEventProcessorMixin):
    """ A mix-in class that adds functionality to BaseWidgets. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        KeyEventProcessorMixin.__init__(self)

        self.bind("<KeyPress>", self.__on_tk_keydown)
        self.bind("<KeyRelease>", self.__on_tk_keyup)

    ##########
    #   Operations
    @property    
    def enabled(self):
        """ True if this Button is enabled, False if disabled. """
        return tk.DISABLED not in self.state()

    @enabled.setter
    def enabled(self, yes: bool):
        """ 
            Enables or disables this BasePlugin.
            
            @param value:
                True to enable this BasePlugin, false to disable.
        """
        if yes:
            self.state(["!disabled"])
        else:
            self.state(["disabled"])

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
        self._process_key_event(ke)
        if ke.keychar is not None:
            ce = KeyEvent(self, KeyEventType.KEY_CHAR, evt)
            self._process_key_event(ce)
    
    def __on_tk_keyup(self, evt: tk.Event):
        #print(evt)
        ke = KeyEvent(self, KeyEventType.KEY_UP, evt)
        self._process_key_event(ke)
            