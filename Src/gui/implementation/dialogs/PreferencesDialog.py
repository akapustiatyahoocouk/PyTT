#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources
from ..misc.GuiSettings import GuiSettings

##########
#   Public entities
@final
class PreferencesDialogResult(Enum):
    """ The result of modal invocation of the PreferencesDialog. """

    OK = 1
    """ User has changed and saved the preferences. """

    CANCEL = 2
    """ Dialog cancelled by user. """

class PreferencesDialog(Dialog):
    """ The modal "Preferences" dialog. """
    
    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Dialog.__init__(self, parent, GuiResources.string("PreferencesDialog.Title"))

        self.__result = PreferencesDialogResult.CANCEL
        
        #   Save preference values in case we need to rollback them
        self.__saved_preference_values = dict()
        self.__record_preference_values(Preferences.ROOT)

        #   Create control styles
        style = ttk.Style()
        style.layout('Tabless.TNotebook.Tab', []) # new style with tabs turned off

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__preferences_tree_view = TreeView(self.__controls_panel, show="tree", selectmode=tk.BROWSE)

        self.__preferences_panel = Panel(self.__controls_panel)
        self.__current_preferences_label = Label(self.__preferences_panel, text="")
        self.__preferences_tabbed_pane = TabbedPane(self.__preferences_panel, style="Tabless.TNotebook")
        self.__no_preferences_tab_page = Panel(self.__preferences_tabbed_pane)
        self.__preferences_tabbed_pane.add(self.__no_preferences_tab_page)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("PreferencesDialog.OkButton.Text"),
            image=GuiResources.image("PreferencesDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("PreferencesDialog.CancelButton.Text"),
            image=GuiResources.image("PreferencesDialog.CancelButton.Icon"))

        #   Create dynamic controls
        self.__map_preferences_to_editors = dict()
        self.__map_preferences_to_tab_pane_indices = dict()
        self.__populate_preferences_tree(None, Preferences.ROOT)

        #   Adjust control
        self.__preferences_tabbed_pane.focusable = False
        if GuiSettings.current_preferences is not None:
            self.__select_preferences_node(self.__preferences_tree_view.root_nodes, GuiSettings.current_preferences)

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)

        self.__preferences_tree_view.pack(side=tk.LEFT, padx=0, pady=0)
        self.__preferences_panel.pack(fill=tk.BOTH, padx=2, pady=0)
        self.__current_preferences_label.pack(side=tk.TOP, fill=tk.X, padx=2, pady=0)
        self.__preferences_tabbed_pane.pack(fill=tk.BOTH, padx=2, pady=0)

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=0, pady=0)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   TODO select last selected Preferences tree node as current
        
        #   Set up event listeners
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button
        
        self.__preferences_tree_view.add_item_listener(self.__preferences_tree_view_listener)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        current_node = self.__preferences_tree_view.current_node
        preferences = current_node.tag if current_node is not None else None
        editor = self.__map_preferences_to_editors.get(preferences, None)
        
        if preferences is None:
            self.__current_preferences_label.configure(text="")
        else:
            self.__current_preferences_label.configure(text=preferences.qualified_display_name)
        if editor is None:
            self.__preferences_tabbed_pane.select(0)
        else:
            self.__preferences_tabbed_pane.select(self.__map_preferences_to_tab_pane_indices[preferences])
        pass

    ##########
    #   Properties
    @property
    def result(self) -> PreferencesDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __record_preference_values(self, preferences: Preferences):
        for child in preferences.children:  #   TODO sort by explicit order, then alphabetically
            #   Do this child...
            for preference in child.preferences:
                self.__saved_preference_values[preference] = preference.value
            #   ... then sub-children
            self.__record_preference_values(child)

    def __populate_preferences_tree(self, parent_node: TreeNode, preferences: Preferences):
        children = list(preferences.children)
        self.__sort_preferences(children)
        for child in children:
            #   Do this child...
            if parent_node is None:
                child_node = self.__preferences_tree_view.root_nodes.add(child.display_name, tag=child)
            else:
                child_node = parent_node.child_nodes.add(child.display_name, tag=child)
            editor = child.create_editor(self.__preferences_tabbed_pane)
            self.__map_preferences_to_editors[child] = editor
            if editor is not None:
                editor_tab_index = len(self.__preferences_tabbed_pane.tabs())
                self.__preferences_tabbed_pane.add(editor, state="normal", text=preferences.qualified_name)
                self.__map_preferences_to_tab_pane_indices[child] = editor_tab_index
            #   ... then sub-children
            self.__populate_preferences_tree(child_node, child)

    def __sort_preferences(self, elements: List[Preferences]) -> None:
        if len(elements) <= 1:
            return  # no point in sorting!
        sorted_by_order = list(filter(lambda p: p.sort_order is not None, elements))
        sorted_by_name = list(filter(lambda p: p.sort_order is None, elements))
        sorted_by_order.sort(key=lambda p: p.sort_order)
        sorted_by_name.sort(key=lambda p: p.display_name)
        elements.clear()
        elements.extend(sorted_by_order)
        elements.extend(sorted_by_name)
    
    def __select_preferences_node(self, parent_nodes: TreeNodeCollection, preferences: Preferences) -> bool:
        for node in parent_nodes:
            if node.tag == preferences:
                self.__preferences_tree_view.see(node._TreeNode__tk_node_id)    #   TODO use awt.TreeView API
                self.__preferences_tree_view.selection_set([node._TreeNode__tk_node_id])    #   TODO use awt.TreeView API
                self.request_refresh()
                return True
            if self.__select_preferences_node(node.child_nodes, preferences):
                return True
        return False
            
    def __apply_preferences(self, preferences: Preferences):
        children = list(preferences.children)
        for child in children:
            #   Do this child...
            child.apply()
            #   ... then sub-children
            self.__apply_preferences(child)

    ##########
    #   Event listeners
    def __preferences_tree_view_listener(self, evt: ItemEvent):
        current_node = self.__preferences_tree_view.current_node
        preferences = current_node.tag if current_node is not None else None
        GuiSettings.current_preferences = preferences
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        if not self.__ok_button.enabled:
            return
        self.__apply_preferences(Preferences.ROOT)
        self.__result = PreferencesDialogResult.OK
        self.end_modal()

    def __on_cancel(self, evt = None) -> None:
        #   Rollback changes made to preferences
        for preference in self.__saved_preference_values:
            preference.value = self.__saved_preference_values[preference]
        self.__result = PreferencesDialogResult.CANCEL
        self.end_modal()
