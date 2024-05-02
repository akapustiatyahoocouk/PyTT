""" Defines a list box UI widget. """
#   Python standard library
from typing import Optional, Any
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .Panel import Panel
from .TreeView import TreeView
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class ListBoxItem:
    """ A single itemof a ListBox. Can be either free (not
        currently used by any ListBox) or bound (used by
        exactly 1 ListBox. All ListBoxItems are created as free
        ListBox items and are then addedd to a ListBox, binding
        them there, although some services can combine these 2
        operations in one call. """

    ##########
    #   Construction
    def __init__(self, text: str = "", tag: Any = None) -> None:
        assert isinstance(text, str)

        self.__text = text
        self.__tag = tag

        self.__list_box = None #   None for free combo box items

    ##########
    #   Properties
    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, new_text: str) -> None:
        assert isinstance(new_text, str)
        if new_text != self.__text:
            self.__text = new_text
            if self.__list_box is not None:
                #   Must update the text of the underlying TreeNode
                index = self.__list_box._ListBox__items.index(self)
                tree_node = self.__list_box._ListBox__items._ListBoxItems__tree_view_items[index]
                tree_node.text = new_text

    @property
    def tag(self) -> Any:
        return self.__tag

    @tag.setter
    def tag(self, tag: Any) -> None:
        self.__tag = tag
    
    @property
    def list_box(self) -> "ListBox":
        return self.__list_box

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
        self.__tree_view_items = [] #   Parallel to self.__items

    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__items)

    def __getitem__(self, index: int) -> ListBoxItem:
        assert isinstance(index, int)
        return self.__items[index]

    ##########
    #   Operations
    def add(self, item, tag: Any = None) -> ListBoxItem:
        """
            Adds the specified item to the end of the list
            of items of the ListBox.

            @param item:
                The item to add to the ListBox.
            @param tag:
                The tag to add to a new str-based item.
            @return:
                The newly added LisyBoxItem.
        """
        loc = locals()
        if isinstance(item, str):
            #   Create a new, initially bound, list box item
            new_item = ListBoxItem(item, tag)
            assert new_item.list_box is None
            self.__items.append(new_item)
            new_item._ListBoxItem__list_box = self.__list_box
            #   Create the underlying TreeView item
            tree_view_item = self.__list_box._ListBox__tree_view.root_nodes.add(item, tag=new_item)
            self.__tree_view_items.append(tree_view_item)
            #   Done assing a new ListBoxItem
            return new_item
        elif isinstance(item, ListBoxItem):
            #   The item must NOT already be bound
            assert item.list_box is None
            raise NotImplementedError()
        else:
            raise ValueError(str(loc))

        item_id = self.__list_box._ListBox__tree_view.insert("", "end", text=str(item))
        self.__items.append(item)
        self.__item_ids.append(item_id)
        return len(self.__items) - 1

    def index(self, element):
        return self.__items.index(element)

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

        self.__tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE, **kwargs)
        #   TODO scrollbars

        #   Set up control structure
        self.__tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #   Set up event handlers
        self.__tree_view.add_item_listener(self.__tree_view_item_listener)

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
        current_node = self.__tree_view.current_node
        if current_node is None:
            return None
        return self.__tree_view.root_nodes.index(current_node)

    @selected_index.setter
    def selected_index(self, new_index: Optional[int]) -> None:
        assert (new_index is None) or isinstance(new_index, int)

        try:
            old_index = self.selected_index
            if new_index is None:
                for item in self.__tree_view.selection():
                    self.__tree_view.selection_remove(item)
            else:
                assert 0 <= new_index < len(self.__items)
                tree_node_id = self.__items._ListBoxItems__tree_view_items[new_index]._TreeNode__tk_node_id
                self.__tree_view.selection_set(tree_node_id)
            new_index = self.selected_index
            if new_index != old_index:
                if old_index is not None:
                    self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
                if new_index is not None:
                    self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        except Exception:
            pass    #   Index out of range - don't change it

    @property
    def selected_item(self) -> Any:
        """ The currently selected list box item, or None if no
            item is currently selected. """
        index = self.selected_index
        return None if index is None else self.__items[index]

    ##########
    #   Tk event handlers
    def __tree_view_item_listener(self, evt: ItemEvent):
        assert isinstance(evt, ItemEvent)
        if self.__tree_view.current_node is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
