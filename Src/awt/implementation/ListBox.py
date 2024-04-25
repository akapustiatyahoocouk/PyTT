"""
    Defines a list box UI widget.
"""
#   Python standard library
from typing import Callable, Optional, Any
from inspect import signature
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .Widget import Widget
from .Panel import Panel
from .TreeView import TreeView
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class ListBoxItems:
    """ The ordered collection of all items currently in the ListBox. """

    ##########
    #   Construction (internal)
    def __init__(self, list_box: ttk.Widget):
        """ Constructs the list box items collection (internal use only). """
        assert isinstance(list_box, ListBox)
        assert list_box._ListBox__creating_items

        self.__list_box = list_box
        self.__items = []
        self.__item_ids = []    #   Parallel to self.__items

    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__items)

    def __getitem__(self, index: int) -> Any:
        assert isinstance(index, int)
        return self.__items[index]

    ##########
    #   Properties
    @property
    def length(self) -> int:
        """ The number of items in the ListBox. """
        return len(self.__items)

    ##########
    #   Operations
    def add(self, item) -> int:
        """
            Adds the specified item to the end of the list
            of items of the ListBox.

            @param item:
                The item to add to the ListBox, can be anything
                except None. The str(item) will appear in the UI.
        """
        assert item is not None

        item_id = self.__list_box._ListBox__tree_view.insert("", "end", text=str(item))
        self.__items.append(item)
        self.__item_ids.append(item_id)
        return len(self.__items) - 1

class ListBox(Panel,
              ItemEventProcessorMixin):
    """ A ttk.Treeview that behaves as a list box. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt ListBox widget with the parent master. """
        Panel.__init__(self, master, **kwargs)
        ItemEventProcessorMixin.__init__(self)

        self.__creating_items = True
        self.__items = ListBoxItems(self)
        self.__creating_items = False

        self.__tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        #scrollbar.pack(side="right", fill="y")
        self.__tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #   Set up event handlers
        self.__tree_view.bind("<<TreeviewSelect>>", self.__on_tk_treeview_selected)

    ##########
    #   BaseWidgetMixin
    #   TODO visible, focusable, etc. properties must delegate to
    #   the self.__tree_view!

    ##########
    #   Properties
    @property
    def items(self) -> ListBoxItems:
        """ The ordered collection of items in this ListBox. """
        return self.__items

    @property
    def selected_index(self) -> Optional[int]:
        """ The 0-based index of the currently selected list box
            item, or None if no item is currently selected. """
        try:
            item_id = self.__tree_view.focus()
            item_index = self.__items._ListBoxItems__item_ids.index(item_id)
            return item_index
        except:
            return None

    @selected_index.setter
    def selected_index(self, new_index: Optional[int]) -> None:
        assert (new_index is None) or isinstance(new_index, int)

        try:
            old_index = self.selected_index
            if new_index is None:
                for item in self.__tree_view.selection():
                    self.__tree_view.selection_remove(item)
            else:
                assert new_index >= 0 and new_index < len(self.__items)
                self.__tree_view.selection_set(new_index)
            new_index = self.selected_index
            if new_index != old_index:
                if old_index is not None:
                    self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
                if new_index is not None:
                    self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        except:
            pass    #   Index out of range

    @property
    def selected_item(self) -> Any:
        """ The currently selected list box item, or None if no
            item is currently selected. """
        index = self.selected_index
        return None if index is None else self.__items[index]

    ##########
    #   Tk event handlers
    def __on_tk_treeview_selected(self, evt: tk.Event):
        if self.selected_index is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
