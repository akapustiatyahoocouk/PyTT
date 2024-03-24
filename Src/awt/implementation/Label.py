""" A ttk.Label with AWT extensions. """
#   Python standard library
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class Label(ttk.Label, BaseWidgetMixin):
    """ A ttk.Label with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Label widget with the parent master. """
        ttk.Label.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)

        self.focusable = False
