#   Python standard library
from typing import Optional, Any
from inspect import signature
import tkinter as tk

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
        if TextField.__text_impl is None:
            TextField.__text_impl = "TEXT"
        return TextField.__text_impl

    ##########
    #   Construction
    def __init__(self, parent=None, text: str="", **kwargs):
        """ Construct an awt TextArea widget with the specified parent. """
        tk.Text.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        PropertyChangeEventProcessorMixin.__init__(self)

        assert isinstance(text, str)
        
        self.insert('end', text)
        self.delete('1.0', tk.END)
        self.insert('end', text)
        t2 = self.get('1.0', 'end-1c')  #   The right one!!!
        
        pass
        #self.__variable = tk.StringVar(master=self, value=text)
        #self.configure(textvariable=self.__variable)

        #   Set up event handlers
        #self.__variable.trace_add("write", self.__on_tk_text_changed)

    ##########
    #   ttk emulation
    def state(self) -> Any:
        return ()    
    