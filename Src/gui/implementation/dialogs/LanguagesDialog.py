""" Implements "About PyTT" modal dialog. """
#   Python standard library
from typing import final
from enum import Enum
import tkinter as tk
import idlelib.redirector as rd

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class LanguagesDialog(Dialog):
    """ The modal "Languages" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("LanguagesDialog.Title"))

        all_locales = list(LocalizableSubsystem.all_supported_locales())
        all_locales.sort(key=lambda locale: repr(locale))
        
        #   Create controls
        self.__controls_panel = Panel(self)
        self.__languages_tree_view = TreeView(self.__controls_panel, selectmode=tk.NONE)
        
        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("LanguagesDialog.OkButton.Text"),
            image=GuiResources.image("LanguagesDialog.OkButton.Icon"))

        #   Adjust controls
        columns = list(map(lambda locale: str(locale), all_locales))
        self.__languages_tree_view['columns'] = columns
        for key in columns:
            self.__languages_tree_view.heading(key, text=key)
            self.__languages_tree_view.column(key, anchor=tk.CENTER)
        self.__add_component_row(Subsystem.ROOT, all_locales)
            
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__languages_tree_view.pack(fill=tk.BOTH, padx=0, pady=0)
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__ok_button

        self.__ok_button.add_action_listener(self.__on_ok)

        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Implementation helpers
    def __add_component_row(self, subsystem: Subsystem.ROOT, all_locales: List[Locale]) -> None:
        #   Prepare locale support map for the "subsystem"
        supported_locales = Locale.ROOT
        if isinstance(subsystem, LocalizableSubsystem):
            supported_locales = subsystem.supported_locales
        locale_support = list(map(lambda l: "\u2611" if l in supported_locales else "\u2610", all_locales))
        #   ...then insert this node...
        self.__languages_tree_view.insert(parent="", index="end", 
                                          text=subsystem.qualified_display_name,
                                          values=locale_support)
        #   ...then do the children
        children = list(subsystem.children)
        children.sort(key=lambda c: c.display_name)
        for child in children:    #   TODO sort by display name
            self.__add_component_row(child, all_locales)
    
    ##########
    #   Event listeners    
    def __on_ok(self, evt = None) -> None:
        self.end_modal()
