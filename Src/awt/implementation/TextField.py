""" A ttk.Entry with AWT extensions. """

#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk
import idlelib.redirector as rd

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class TextField(ttk.Entry,
                BaseWidgetMixin,
                PropertyChangeEventProcessorMixin):
    """ A ttk.Entry with AWT extensions. """

    ##########
    #   Constants
    __text_impl = None
    @staticproperty
    def TEXT() -> str:
        """ The name of the "TEXT" property of this text field. """
        if TextField.__text_impl is None:
            TextField.__text_impl = "TEXT"
        return TextField.__text_impl

    ##########
    #   Construction
    def __init__(self, parent=None, text: str="", **kwargs):
        """ Construct an awt TextField widget with the specified parent. """
        ttk.Entry.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        PropertyChangeEventProcessorMixin.__init__(self)

        assert isinstance(text, str)

        self.__variable = tk.StringVar(master=self, value=text)
        self.configure(textvariable=self.__variable)

        self.__readonly = False

        #   Set up event handlers
        self.__variable.trace_add("write", self.__on_tk_text_changed)
        self.redirector = rd.WidgetRedirector(self)

    ##########
    #   Properties
    @property
    def text(self) -> str:
        """ The text content of this text field. """
        return self.__variable.get()

    @text.setter
    def text(self, new_text: str) -> None:
        """ Sets the text content of this text field. """
        assert isinstance(new_text, str)
        self.__variable.set(new_text)

    @property
    def password_entry(self) -> bool:
        """ True if this TextField is a hidden password entry
            field, False if it is a plain text entry field (default). """
        raise NotImplementedError

    @password_entry.setter
    def password_entry(self, new_password_entry: bool) -> None:
        """ Makes this TextField a hidden password entry field (True),
            or a plain text entry field (False). """
        assert isinstance(new_password_entry, bool)
        self.configure(show="\u2022" if new_password_entry else None)

    @property
    def readonly(self) -> bool:
        """ True if this TextField is read-only, False if
            modifiable by the user (default). """
        return self.__readonly

    @readonly.setter
    def readonly(self, new_readonly: bool) -> None:
        """ Makes this TextField read-only (True), or modifiable
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

    ##########
    #   Tk event handlers
    def __on_tk_text_changed(self, *_):
        evt = PropertyChangeEvent(source=self,
                                  affected_object=self,
                                  changed_property=TextField.TEXT)
        self.process_property_change_event(evt)
