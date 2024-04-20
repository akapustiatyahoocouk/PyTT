#   Python standard library
from typing import Callable
from inspect import signature
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class TreeView(ttk.Treeview, BaseWidgetMixin):
    """ A ttk.Treeview with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt TreeView widget with the parent master. """
        ttk.Treeview.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
