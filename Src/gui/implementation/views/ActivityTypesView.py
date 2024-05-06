#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .ActivityTypesViewType import ActivityTypesViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class ActivityTypesView(View):
    
    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls
        
        self.__activity_types_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.CreateActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.CreateActivityTypeButton.Image"))
        self.__modify_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.ModifyActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.ModifyActivityTypeButton.Image"))
        self.__destroy_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.DestroyActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.DestroyActivityTypeButton.Image"))
        
        #   Adjust controls
        self.__activity_types_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__activity_types_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        self.__create_activity_type_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_activity_type_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_activity_type_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return ActivityTypesViewType.instance

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.CreateActivityTypeButton.Text")
        self.__modify_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.ModifyActivityTypeButton.Text")
        self.__destroy_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.DestroyActivityTypeButton.Text")


    ##########
    #   Event handlers
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__apply_default_locale()
        self.request_refresh()
    