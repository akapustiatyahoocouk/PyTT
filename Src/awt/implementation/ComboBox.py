""" Defines a combo box (drop-down list, potentially editable) UI widget. """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, Any
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class ComboBoxItem:
    """ A single itemof a ComboBox. Can be either free (not
        currently used by any ComboBox) or bound (used by
        exactly 1 ComboBox. All ComboBoxItems are created as free
        ComboBox items and are then addedd to a ComboBox, binding
        them there, although some services can combine these 2
        operations in one call. """

    ##########
    #   Construction
    def __init__(self, text: str = "", tag: Any = None) -> None:
        assert isinstance(text, str)

        self.__text = text
        self.__tag = tag

        self.__combo_box= None #   None for free combo box items

    ##########
    #   Properties
    @property
    def text(self) -> str:
        """ The text of this combo box item. """
        return self.__text

    @property
    def tag(self) -> Any:
        """ The tag of this combo box item. """
        return self.__tag

    @property
    def combo_box(self) -> ComboBox:
        """ The combo box to which this item is bound;None if free. """
        return self.__combo_box

class ComboBoxItems:
    """ An ordered list of items of a ComboBox. """

    ##########
    #   Construction (internal)
    def __init__(self, combo_box: ttk.Combobox):
        assert isinstance(combo_box, ComboBox)
        assert combo_box._ComboBox__creating_items

        self.__combo_box = combo_box
        self.__items = []

    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__items)

    def __getitem__(self, index: int) -> Any:
        assert isinstance(index, int)
        return self.__items[index]

    ##########
    #   Operations
    def add(self, item, tag: Any = None) -> ComboBoxItem:
        """
            Adds the specified item to the end of this collection of
            ComboBox items.

            @param item:
                The item to add; cannot be None.
            @param tag:
                The tag to add to a new str-based item.
            @return:
                The newly added item.
        """
        loc = locals()
        if isinstance(item, str):
            #   Create a new, initially bound, combo box item
            new_item = ComboBoxItem(item, tag)
            assert new_item.combo_box is None
            self.__items.append(new_item)
            new_item._ComboBoxItem__combo_box = self.__combo_box
            self.__combo_box["values"] = (*self.__combo_box["values"], item)
            return new_item
        elif isinstance(item, ComboBoxItem):
            #   The item must NOT already be bound
            assert item.combo_box is None
            raise NotImplementedError()
        else:
            raise ValueError(str(loc))

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
        """ True if this combo box shall be editable, False if it
            shall behave as a non-editable drop-down list. """
        return "readonly" in self.state()

    @editable.setter
    def editable(self, yes: bool):
        """
            Makes this combo box editable or drop-down.

            @param value:
                True to make this combo box editable, false to make
                it a drop-down list.
        """
        if yes:
            self.state(["!readonly"])
        else:
            self.state(["readonly"])

    @property
    def items(self) -> ComboBoxItems:
        """ The ordered collection of items in this combo box. """
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
        except Exception:
            pass    #   Index out of range

    @property
    def selected_item(self) -> Any:
        """ The combo box item currently selected, None == none. """
        index = self.current()
        if (index is None) or (index == -1):
            return None
        return self.__items[index]

    @selected_item.setter
    def selected_item(self, new_item: Optional[ComboBoxItem]) -> None:
        assert (new_item is None) or isinstance(new_item, ComboBoxItem)

        if new_item is None:
            self.selected_index = -1
        elif new_item in self.__items._ComboBoxItems__items:
            self.selected_index = self.__items._ComboBoxItems__items.index(new_item)

    ##########
    #   Tk event handlers
    def __on_tk_combobox_selected(self, evt: tk.Event):
        assert isinstance(evt, tk.Event)

        if self.selected_index is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
