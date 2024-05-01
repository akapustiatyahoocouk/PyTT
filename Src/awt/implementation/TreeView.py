""" A ttk.Treeview with AWT extensions. """

#   Python standard library
from typing import Any, Optional, List
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventProcessorMixin import ItemEventProcessorMixin

##########
#   Public entities
class TreeNode:
    """ A single node of a TreeView. Can be either free (not
        currently used by any TreeView) or bound (used by
        exactly 1 TreeView. All TreeNodes are created as free
        tree nodes and are then addedd to a TreeView, binding
        them there, although some services can combine these 2
        operations in one call. """

    ##########
    #   Construction
    def __init__(self, text: str = "", image: Optional[tk.PhotoImage] = None, tag: Any = None) -> None:
        assert isinstance(text, str)
        assert (image is None) or isinstance(image, tk.PhotoImage)

        self.__tk_node_id = None    #   always so for free nodes
        self.__text = text
        self.__image = image
        self.__tag = tag

        self.__parent_node = None    #   TreeNode for bound non-root nodes
        self.__child_nodes = TreeNodeCollection(self)
        self.__tree_view = None #   None for free tree nodes

    ##########
    #   Properties
    @property
    def text(self) -> str:
        return self.__text

    @property
    def image(self) -> Optional[tk.PhotoImage]:
        return self.__image

    @property
    def tag(self) -> Any:
        return self.__tag

    @property
    def parent_node(self) -> str:
        return self.__parent_node

    @property
    def child_nodes(self) -> "TreeNodeCollection":
        return self.__child_nodes

    @property
    def tree_view(self) -> "TreeView":
        return self.__tree_view

class TreeNodeCollection:
    """ An ordered collection of tree nodes. """

    ##########
    #   Construction
    def __init__(self, owner: Any) -> None:
        assert isinstance(owner, TreeNode) or isinstance(owner, TreeView)

        self.__owner = owner
        self.__members = []

    def __len__(self) -> int:
        return len(self.__members)
    
    def __getitem__(self, index: int) -> Any:
        assert isinstance(index, int)
        return self.__members[index]

    def __iter__(self) -> "SqlRecordSet":
        return self.__members.copy().__iter__()

    #TODO kill off
    #def __next__(self) -> SqlRecord:
    #    if self.__current_row < len(self.__rows):
    #        row = self.__rows[self.__current_row]
    #        self.__current_row += 1
    #        return SqlRecord(self, row)
    #    else:
    #        raise StopIteration

    ##########
    #   Operations
    def add(self, item: Any, image: Optional[tk.PhotoImage] = None, tag: Any = None) -> TreeNode:
        loc = locals()
        if isinstance(item, str):
            #   Create a new, initially bound, tree node
            node = TreeNode(item, image, tag)
            assert node.tree_view is None
            assert node.parent_node is None
            #   Add the newly created tree node to this tree node collection
            self.__members.append(node)
            if isinstance(self.__owner, TreeNode):
                node._TreeNode__parent_node = self.__owner
            #   If this tree node collection is part of a TreeView,
            #   bind the newly created node to the TreeView
            if isinstance(self.__owner, TreeNode) and (self.__owner.tree_view is not None):
                #   This is a collection of child nodes of a TreeNode
                #   that is already bound to a TreeView
                node._TreeNode__tree_view = self.__owner.tree_view
                #   Add Tk tree node to the underlying control
                if image is None:
                    node._TreeNode__tk_node_id = self.__owner.tree_view.insert(self.__owner._TreeNode__tk_node_id, tk.END, text=item)
                else:
                    node._TreeNode__tk_node_id = self.__owner.tree_view.insert(self.__owner._TreeNode__tk_node_id, tk.END, text=item, image=image)
            elif isinstance(self.__owner, TreeView):
                #   This is a collection of root nodes of a TreeView
                node._TreeNode__tree_view = self.__owner
                #   Add Tk tree node to the underlying control
                if image is None:
                    node._TreeNode__tk_node_id = self.__owner.insert("", tk.END, text=item)
                else:
                    node._TreeNode__tk_node_id = self.__owner.insert("", tk.END, text=item, image=image)
            #   Done assing a new TreeNode
            return node
        elif isinstance(item, TreeNode):
            #   The node must NOT already be bound
            assert node.tree_view is None
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def clear(self) -> None:
        while len(self.__members) > 0:
            member_node = self.__members[0]
            self.__members.pop()
            #   Mist delete all child nodes of the member_node
            member_node.child_nodes.clear()
            #   Remove the underlying Tk node...
            tree_view = member_node._TreeNode__tree_view
            if tree_view is not None:
                tree_view.delete(member_node._TreeNode__tk_node_id) #   member_node was bound...
                member_node._TreeNode__tree_view = None             #   ...and is now free
                member_node._TreeNode__tk_node_id = None
            else:
                assert member_node._TreeNode__tk_node_id is None    #   ...for consistency
            #   ...and adjust the TreeNode to reflect ots removal from the tree
            member_node._TreeNode__parent_node

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

        self.__root_nodes = TreeNodeCollection(self)

        #   Set up event handlers
        self.bind("<<TreeviewSelect>>", self.__on_tk_treeview_selected)

    ##########
    #   Properties
    @property
    def root_nodes(self) -> TreeNodeCollection:
        return self.__root_nodes

    @property
    def current_node(self) -> Optional[TreeNode]:
        """ The currently highlighted tree node, None if there isn't one. """
        focus = self.selection()
        return self.__find_tree_node_by_tk_id(self.__root_nodes, focus[0]) if len(focus) > 0 else None

    ##########
    #   Implementation heipers
    def __find_tree_node_by_tk_id(self, nodes: TreeNodeCollection, tk_node_id: str) -> Optional[TreeNode]:
        for node in nodes:
            if node._TreeNode__tk_node_id == tk_node_id:
                return node
            found = self.__find_tree_node_by_tk_id(node.child_nodes, tk_node_id)
            if found is not None:
                return found
        return None

    ##########
    #   Tk event handlers
    def __on_tk_treeview_selected(self, evt: tk.Event):
        assert isinstance(evt, tk.Event)
        if self.current_node is not None:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_SELECTED))
        else:
            self.process_item_event(ItemEvent(self, ItemEventType.ITEM_UNSELECTED))
