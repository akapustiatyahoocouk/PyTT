#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .UsersViewType import UsersViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class UsersView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__users_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.CreateUserButton.Text"),
            image=GuiResources.image("UsersViewEditor.CreateUserButton.Image"))
        self.__modify_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.ModifyUserButton.Text"),
            image=GuiResources.image("UsersViewEditor.ModifyUserButton.Image"))
        self.__destroy_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.DestroyUserButton.Text"),
            image=GuiResources.image("UsersViewEditor.DestroyUserButton.Image"))

        self.__create_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.CreateAccountButton.Text"),
            image=GuiResources.image("UsersViewEditor.CreateAccountButton.Image"))
        self.__modify_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.ModifyAccountButton.Text"),
            image=GuiResources.image("UsersViewEditor.ModifyAccountButton.Image"))
        self.__destroy_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersViewEditor.DestroyAccountButton.Text"),
            image=GuiResources.image("UsersViewEditor.DestroyAccountButton.Image"))

        #   Adjust controls
        self.__users_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__users_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__create_user_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_user_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_user_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")
        self.__create_account_button.grid(row=3, column=0, padx=0, pady=(10, 2), sticky="WE")
        self.__modify_account_button.grid(row=4, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_account_button.grid(row=5, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

    ##########
    #   Refreshable    
    def refresh(self) -> None:
        self.__refresh_user_nodes()
        
    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return UsersViewType.instance

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_user_button.text = GuiResources.string("UsersViewEditor.CreateUserButton.Text")
        self.__modify_user_button.text = GuiResources.string("UsersViewEditor.ModifyUserButton.Text")
        self.__destroy_user_button.text = GuiResources.string("UsersViewEditor.DestroyUserButton.Text")

        self.__create_account_button.text = GuiResources.string("UsersViewEditor.CreateAccountButton.Text")
        self.__modify_account_button.text = GuiResources.string("UsersViewEditor.ModifyAccountButton.Text")
        self.__destroy_account_button.text = GuiResources.string("UsersViewEditor.DestroyAccountButton.Text")
        
    ##########
    #   Event handlers
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__apply_default_locale()
        self.request_refresh()
        
    def __refresh_user_nodes(self) -> None:
        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__users_tree_view.root_nodes.clear()
            return
        users = workspace.get_users(credentials)
        
    