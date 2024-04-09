#   Python standard library
from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class Panel(ttk.Frame, BaseWidgetMixin):
    """ A ttk.Frame with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget = None, **kwargs):
        """Construct an awt Panel widget with the specified parent. """
        ttk.Frame.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)

        self.configure(borderwidth = 0)
        self.focusable = False
