from typing import Callable
from inspect import signature

import tkinter.ttk as ttk

from awt_impl.BaseWidgetMixin import BaseWidgetMixin

class Entry(ttk.Entry, BaseWidgetMixin):
    """ A ttk.Entry with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Entry widget with the parent master. """
        ttk.Entry.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
