from typing import Callable
from inspect import signature

import tkinter.ttk as ttk

from awt_impl.BaseWidgetMixin import BaseWidgetMixin

class Widget(ttk.Widget, BaseWidgetMixin):
    """ A ttk.Widget with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Widget widget with the parent master. """
        ttk.Label.__init__(self, master, **kwargs)
        awt_impl.BaseWidgetMixin.BaseWidgetMixin.__init__(self)
