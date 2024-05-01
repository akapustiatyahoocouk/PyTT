#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .ActivityTypesViewType import ActivityTypesViewType
from .View import View

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

        self.__create_activity_type_button = Button(self.__actions_panel, text="Create activity type")
        self.__modify_activity_type_button = Button(self.__actions_panel, text="Modify activity type")
        self.__destroy_activity_type_button = Button(self.__actions_panel, text="Destroy activity type")
        
        #   Adjust controls
        self.__activity_types_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__activity_types_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        self.__create_activity_type_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_activity_type_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_activity_type_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return ActivityTypesViewType.instance
    