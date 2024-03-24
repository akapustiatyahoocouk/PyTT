from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

import awt_impl.BaseWidgetMixin

class Widget(ttk.Widget, 
             awt_impl.BaseWidgetMixin.BaseWidgetMixin):
    """ A ttk.Widget with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Widget widget with the parent master. """
        ttk.Label.__init__(self, master, **kwargs)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
