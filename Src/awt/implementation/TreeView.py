#   Python standard library
from typing import Callable
from inspect import signature
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class TreeView(ttk.Treeview, 
               BaseWidgetMixin,
               ItemEventProcessorMixin):
    """ A ttk.Treeview with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        """Construct an awt TreeView widget with the parent master. """
        ttk.Treeview.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        ItemEventProcessorMixin.__init__(self)
        
        #   Set up event handlers
        self.bind("<<TreeviewSelect>>", self.__on_tk_treeview_selected)
    
    ##########
    #   Properties
    def focused_item(self) -> str:
        """ The ID of the currently focused item, None if there isn't one. """
        focus = self.focus()
        return focus if focus != "" else None

    ##########
    #   Tk event handlers
    def __on_tk_treeview_selected(self, evt: tk.Event):
        if self.focused_item is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
