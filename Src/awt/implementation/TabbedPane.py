""" A ttk.Notebook with AWT extensions. """
#   Python standard library
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class TabbedPane(ttk.Notebook, BaseWidgetMixin):
    """ A ttk.Notebook with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt TabbedPane widget with the parent master. """
        ttk.Notebook.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
