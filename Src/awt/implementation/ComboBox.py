"""
    Defines a combo box (drop-down list, potentially editable)
    UI widget.
"""
#   Python standard library
from typing import Callable, Optional, Any
from inspect import signature
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class ComboBoxItems:

    ##########
    #   Construction (internal)
    def __init__(self, combo_box: ttk.Combobox):
        assert isinstance(combo_box, ComboBox)
        assert combo_box._ComboBox__creating_items

        self.__combo_box = combo_box
        self.__items = list()

    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__items)

    def __getitem__(self, index: int) -> Any:
        assert isinstance(index, int)
        return self.__items[index]

    ######
    #   Properties
    @property
    def length(self) -> int:
        return len(self.__items)

    ##########
    #   Operations
    def add(self, item) -> int:
        assert item is not None

        self.__items.append(item)
        self.__combo_box["values"] = (*self.__combo_box["values"], item)
        return len(self.__items) - 1

class ComboBox(ttk.Combobox,
               BaseWidgetMixin,
               ItemEventProcessorMixin):
    """ A ttk.Combobox with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt ComboBox widget with the parent master. """
        ttk.Combobox.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
        ItemEventProcessorMixin.__init__(self)

        self.__creating_items = True
        self.__items = ComboBoxItems(self)
        self.__creating_items = False

        #   Set up event handlers
        self.bind("<<ComboboxSelected>>", self.__on_tk_combobox_selected)
    ##########
    #   Properties
    @property
    def editable(self) -> bool:
        return "readonly" in self.state()

    @editable.setter
    def editable(self, yes: bool):
        """
            Makes this combo box editable or drop-down.

            @param value:
                True to make this combo box editable, false to make it a drop-down list.
        """
        if yes:
            self.state(["!readonly"])
        else:
            self.state(["readonly"])

    @property
    def items(self) -> ComboBoxItems:
        return self.__items

    @property
    def selected_index(self) -> Optional[int]:
        """ The 0-based index of the currently selected combo box
            item, or None if no item is currently selected. """
        index = self.current()
        return None if (index is None) or (index == -1) else index

    @selected_index.setter
    def selected_index(self, new_index: Optional[int]) -> None:
        assert (new_index is None) or isinstance(new_index, int)

        try:
            old_index = self.selected_index
            self.current(new_index)
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
        index = self.current()
        if (index is None) or (index == -1):
            return None
        return self.__items[index]

    ##########
    #   Tk event handlers
    def __on_tk_combobox_selected(self, evt: tk.Event):
        if self.selected_index is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
