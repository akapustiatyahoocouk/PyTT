#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .UsersViewType import UsersViewType
from .View import View

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

        self.__create_user_button = Button(self.__actions_panel, text="Create user")
        self.__modify_user_button = Button(self.__actions_panel, text="Modify user")
        self.__destroy_user_button = Button(self.__actions_panel, text="Destroy user")
        
        self.__create_account_button = Button(self.__actions_panel, text="Create account")
        self.__modify_account_button = Button(self.__actions_panel, text="Modify account")
        self.__destroy_account_button = Button(self.__actions_panel, text="Destroy account")

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

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return UsersViewType.instance
    