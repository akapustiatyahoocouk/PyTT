#   Python standard library
from typing import Callable
from inspect import signature
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class Widget(ttk.Widget, BaseWidgetMixin):
    """ A ttk.Widget with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Widget widget with the parent master. """
        ttk.Label.__init__(self, master, **kwargs)
        BaseWidgetMixin.BaseWidgetMixin.__init__(self)
