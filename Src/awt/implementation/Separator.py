#   Python standard library
from typing import Callable
from inspect import signature

import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class Separator(ttk.Separator, BaseWidgetMixin):
    """ A ttk.Separator with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Separator widget with the parent master. """
        ttk.Separator.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)

        self.configure(takefocus=0)
