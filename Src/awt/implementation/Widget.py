""" A ttk.Widget with AWT extensions. """
#   Python standard library
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
        ttk.Widget.__init__(self, master, widgetname=".www", **kwargs)
        BaseWidgetMixin.BaseWidgetMixin.__init__(self)
