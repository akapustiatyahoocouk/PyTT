#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class PreferencesDialog(Dialog):
    
    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Dialog.__init__(self, parent, GuiResources.string("PreferencesDialog.Title"))
        
        #   Create control styles
        style = ttk.Style()
        style.layout('Tabless.TNotebook.Tab', []) # new style with tabs turned off

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__preferences_tree_view = TreeView(self.__controls_panel, show="tree", selectmode=tk.BROWSE)
        
        self.__preferences_panel = Panel(self.__controls_panel)
        self.__current_preferences_label = Label(self.__preferences_panel, text="")
        self.__preferences_tabbed_pane = TabbedPane(self.__preferences_panel, style="Tabless.TNotebook")
        
        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("PreferencesDialog.OkButton.Text"),
            image=GuiResources.image("PreferencesDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("PreferencesDialog.CancelButton.Text"),
            image=GuiResources.image("PreferencesDialog.CancelButton.Icon"))

        #   Create dynamic controls
        self.__map_preferences_to_editors = dict()
        self.__populate_preferences_tree("", Preferences.ROOT)
        
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        
        self.__preferences_tree_view.pack(side=tk.LEFT, padx=0, pady=0)
        self.__preferences_panel.pack(fill=tk.BOTH, padx=0, pady=0)
        self.__current_preferences_label.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        self.__preferences_tabbed_pane.pack(fill=tk.BOTH, padx=0, pady=0)
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=0, pady=0)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event listeners     
        self.__preferences_tree_view.add_item_listener(self.__preferences_tree_view_listener)
        
        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Implementation helpers
    def __populate_preferences_tree(self, parent_item: str, preferences: Preferences):
        for child in preferences.children:  #   TODO sort by explicit order, then alphabetically
            #   Do this child...
            child_node_id = self.__preferences_tree_view.insert(parent_item, tk.END, text=child.display_name)
            editor = child.create_editor(self.__preferences_tabbed_pane)
            self.__map_preferences_to_editors[child] = editor
            if editor is not None:
                self.__preferences_tabbed_pane.add(editor, state="normal", text=preferences.qualified_name)
            #   ... then sub-children
            self.__populate_preferences_tree(child_node_id, child)
       
    ##########
    #   Event listeners
    def __preferences_tree_view_listener(self, evt: ItemEvent):
        focus = self.__preferences_tree_view.focused_item
        pass