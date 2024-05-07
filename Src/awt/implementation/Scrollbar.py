""" A ttk.Scrollbar with AWT extensions. """

#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class Scrollbar(ttk.Scrollbar, BaseWidgetMixin):
    """ A ttk.Scrollbar with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        """Construct an awt Scrollbar widget with the parent master. """
        ttk.Scrollbar.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)

        self.focusable = False

