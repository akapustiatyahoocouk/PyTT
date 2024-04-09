"""
    Implements "Login to PyTT" modal dialog.
"""
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class CreateWorkspaceDialogResult(Enum):
    """ The result of modal invocation of the CreateWorkspaceDialog. """

    OK = 1
    """ User has created a new workspace. """
    
    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class CreateWorkspaceDialog(Dialog, ItemEventHandler):
    """ The modal "create workspace" dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: tk.BaseWidget):
        """
            Constructs the "create workspace" dialog.
        
            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used), 
                None == no parent.
        """
        super().__init__(parent, GuiResources.string("Actions.CreateWorkspace.Name"))

        self.__result = CreateWorkspaceDialogResult.CANCEL
        self.__workspace = None
        
        #   Create controls
        self.__controls_panel = Panel(self)
        
        self.__workspace_type_label = Label(self.__controls_panel, text = 'Workspace type:', anchor=tk.E)
        self.__workspace_type_combo_box = ComboBox(self.__controls_panel)
        
        self.__workspace_address_label = Label(self.__controls_panel, text = 'Workspace address:', anchor=tk.E)
        self.__workspace_address_text_field = TextField(self.__controls_panel, width=40)
        self.__browse_button = Button(self.__controls_panel, 
                                      text=GuiResources.string("CreateWorkspaceDialog.BrowseButton.Text"),
                                      image=GuiResources.image("CreateWorkspaceDialog.BrowseButton.Icon"))
        
        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreateWorkspaceDialog.OkButton.Text"),
            image=GuiResources.image("CreateWorkspaceDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreateWorkspaceDialog.CancelButton.Text"),
            image=GuiResources.image("CreateWorkspaceDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__workspace_type_combo_box.editable = False
        for ws_type in WorkspaceType.all:
            self.__workspace_type_combo_box.items.add(ws_type)
        if len(self.__workspace_type_combo_box.items) > 0:
            self.__workspace_type_combo_box.selected_index = 0  #   TODO last created ws type
        
        self.__workspace_address_text_field.enabled = False
        
        self.__selected_workspace_type = self.__workspace_type_combo_box.selected_item
        self.__selected_workspace_address = None

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)
        
        self.__workspace_type_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__workspace_type_combo_box.grid(row=0, column=1, columnspan=2, padx=2, pady=2, sticky="WE")

        self.__workspace_address_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__workspace_address_text_field.grid(row=1, column=1, padx=2, pady=2, sticky="WE")
        self.__browse_button.grid(row=1, column=2, padx=2, pady=2, sticky="E")
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__workspace_type_combo_box.add_item_listener(self)
        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.__refresh()

    ##########
    #   ItemEventHandler
    def on_item_selected(self, evt: ItemEvent) -> None:
        wt = self.__workspace_type_combo_box.selected_item
        if wt != self.__selected_workspace_type:
            self.__selected_workspace_type = wt
            self.__selected_workspace_address = None
            self.__workspace_address_text_field.configure(text="")
            self.__refresh()

    ##########
    #   Properties    
    @property
    def result(self) -> CreateWorkspaceDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __refresh(self, *args) -> None:
        self.__ok_button.enabled = self.__selected_workspace_address is not None
    
    ##########
    #   Event listeners    
    def __on_ok(self, evt = None) -> None:
        if not self.__ok_button.enabled:
            return
        self.__result = CreateWorkspaceDialogResult.OK
        self.end_modal()

    def __on_cancel(self, evt = None) -> None:
        self.__result = CreateWorkspaceDialogResult.CANCEL
        self.end_modal()
