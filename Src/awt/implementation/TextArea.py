""" A tk.Text with AWT extensions. """

#   Python standard library
from typing import Any
import tkinter as tk
import idlelib.redirector as rd

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class TextArea(tk.Text,
               BaseWidgetMixin,
               PropertyChangeEventProcessorMixin):
    """ A tk.Text with AWT extensions. """

    ##########
    #   Constants
    __text_impl = None
    @staticproperty
    def TEXT() -> str:
        """ The name of the "TEXT" property of this text area. """
        if TextArea.__text_impl is None:
            TextArea.__text_impl = "TEXT"
        return TextArea.__text_impl

    ##########
    #   Construction
    def __init__(self, parent=None, text: str="", **kwargs):
        """ Construct an awt TextArea widget with the specified parent. """
        tk.Text.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        PropertyChangeEventProcessorMixin.__init__(self)

        assert isinstance(text, str)
        self.insert('end', text)

        self.__readonly = False
        #self.__variable = tk.StringVar(master=self, value=text)
        #self.configure(textvariable=self.__variable)

        #   Set up event handlers
        #self.__variable.trace_add("write", self.__on_tk_text_changed)
        self.redirector = rd.WidgetRedirector(self)

    ##########
    #   ttk emulation for AWT;s sake
    def state(self) -> Any:
        """ Simulates ttk "state" handling. """
        return ()   #   disabled, etc.

    ##########
    #   Properties
    @property
    def text(self) -> str:
        """ The text content of this text area; uses '\n'
            for line breaks. """
        return self.get('1.0', 'end-1c')

    @text.setter
    def text(self, new_text: str) -> None:
        """ Sets the text content of this text area; use '\n'
            for line breaks. """
        assert isinstance(new_text, str)
        self.delete('1.0', tk.END)
        self.insert('end', new_text)

    @property
    def readonly(self) -> bool:
        """ True if this TextArea is read-only, False if
            modifiable by the user (default). """
        return self.__readonly

    @readonly.setter
    def readonly(self, new_readonly: bool) -> None:
        """ Makes this TextArea read-only (True), or modifiable
            by the user (False). """
        assert isinstance(new_readonly, bool)
        if new_readonly != self.__readonly:
            self.__readonly = new_readonly
            if new_readonly:
                self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
                self.delete = self.redirector.register("delete", lambda *args, **kw: "break")
            else:
                self.redirector.unregister("insert")
                self.redirector.unregister("delete")
