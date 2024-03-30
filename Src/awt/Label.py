from typing import Callable
from inspect import signature

import tkinter.ttk as ttk

from awt.BaseWidgetMixin import BaseWidgetMixin

class Label(ttk.Label, BaseWidgetMixin):
    """ A ttk.Label with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Label widget with the parent master. """
        ttk.Label.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
        
        self.configure(takefocus=0)
