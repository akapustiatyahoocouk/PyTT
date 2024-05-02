""" Implements the "Create user" modal dialog. """
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

from requests import get

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources
from ..misc.CurrentCredentials import CurrentCredentials
from ..misc.CurrentWorkspace import CurrentWorkspace

##########
#   Public entities
@final
class CreateUserDialogResult(Enum):
    """ The result of modal invocation of the CreateUserDialog. """

    OK = 1
    """ A new BusinessUser has been created in the current workspace. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class CreateUserDialog(Dialog):
    """ The modal "Create user" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, 
                 workspace: Optional[Workspace] = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "create user" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param workspace:
                The workspace to create a new user in; None == use
                the CurrentWorkspace.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("CreateUserDialog.Title"))

        self.__result = CreateUserDialogResult.CANCEL
        self.__created_user = None
        
        #   Resolve workspace & credentials        
        assert (workspace is None) or isinstance(workspace, Workspace)
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__workspace = workspace if workspace is not None else CurrentWorkspace.get()
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__workspace is not None
        assert self.__credentials is not None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__real_name_label = Label(self.__controls_panel,
                                       text=GuiResources.string("CreateUserDialog.RealNameLabel.Text"),
                                       anchor=tk.E)
        self.__real_name_text_field = TextField(self.__controls_panel, width=40)

        self.__enabled_check_box = CheckBox(self.__controls_panel,
                                            text=GuiResources.string("CreateUserDialog.EnabledCheckBox.Text"))

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreateUserDialog.OkButton.Text"),
            image=GuiResources.image("CreateUserDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreateUserDialog.CancelButton.Text"),
            image=GuiResources.image("CreateUserDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__enabled_check_box.checked = True
        
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__real_name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__real_name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__enabled_check_box.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__real_name_text_field.add_property_change_listener(self.__text_field_change_listener)
                                                                
        #self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__ok_button.enabled = len(self.__real_name_text_field.text.strip()) > 0
    
    ##########
    #   Properties
    @property
    def result(self) -> CreateUserDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def created_user(self) -> Optional[BusinessUser]:
        """ The BusinessUser created during dialog invocation;
            None if the dialog was cancelled. """
        return self.__created_user
    
    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        self.request_refresh()

    def __on_cancel(self, evt = None) -> None:
        self.__result = CreateUserDialogResult.CANCEL
        self.end_modal()
