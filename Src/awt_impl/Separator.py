from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

import awt_impl.BaseWidgetMixin
import awt_impl.ActionEvent
import awt_impl.KeyEventProcessorMixin
import awt_impl.ActionEventProcessorMixin

class Separator(ttk.Separator, 
                awt_impl.BaseWidgetMixin.BaseWidgetMixin):
    """ A ttk.Separator with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Separator widget with the parent master. """
        ttk.Separator.__init__(self, master, **kwargs)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
