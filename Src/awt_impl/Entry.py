from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

import awt_impl.BaseWidgetMixin
import awt_impl.ActionEvent
import awt_impl.KeyEventProcessorMixin
import awt_impl.ActionEventProcessorMixin

class Entry(ttk.Entry, 
            awt_impl.BaseWidgetMixin.BaseWidgetMixin):
    """ A ttk.Entry with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Entry widget with the parent master. """
        ttk.Entry.__init__(self, master, **kwargs)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
