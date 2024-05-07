""" Implements the "Create activity type" modal dialog. """

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
from ..controls.EmailAddressListEditor import EmailAddressListEditor

##########
#   Public entities
@final
class CreateActivityTypeDialogResult(Enum):
    """ The result of modal invocation of the CreateActivityTypeDialog. """

    OK = 1
    """ A new BusinessActivityType has been created in the specified workspace. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class CreateActivityTypeDialog(Dialog):
    """ The modal "Create activity type" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 workspace: Optional[Workspace] = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "create activity type" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param workspace:
                The workspace to create a new activity type in; None == use
                the CurrentWorkspace.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("CreateActivityTypeDialog.Title"))

        self.__result = CreateActivityTypeDialogResult.CANCEL
        self.__created_activity_type = None

        #   Resolve workspace & credentials
        assert (workspace is None) or isinstance(workspace, Workspace)
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__workspace = workspace if workspace is not None else CurrentWorkspace.get()
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__workspace is not None
        assert self.__credentials is not None
        
        self.__validator = self.__workspace.validator

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateActivityTypeDialog.NameLabel.Text"),
            anchor=tk.E)
        self.__name_text_field = TextField(self.__controls_panel, width=40)

        self.__description_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateActivityTypeDialog.DescriptionLabel.Text"),
            anchor=tk.E)
        self.__description_text_area = TextArea(self.__controls_panel, height=4, width=40)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreateActivityTypeDialog.OkButton.Text"),
            image=GuiResources.image("CreateActivityTypeDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreateActivityTypeDialog.CancelButton.Text"),
            image=GuiResources.image("CreateActivityTypeDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__description_text_area.accept_tab = False
        
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__description_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__description_text_area.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__name_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__description_text_area.add_property_change_listener(self.__text_field_change_listener)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        #TODO self.__ok_button.enabled = self.__validator.user.is_valid_real_name(self.__real_name_text_field.text)
        pass

    ##########
    #   Properties
    @property
    def result(self) -> CreateActivityTypeDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def created_activity_type(self) -> Optional[BusinessActivityType]:
        """ The BusinessActivityType created during dialog invocation;
            None if the dialog was cancelled. """
        return self.__created_activity_type

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        name = self.__name_text_field.text.strip()
        description = self.__description_text_area.text.rstrip()
        
        try:
            #self.__created_user = self.__workspace.create_user(
            #        credentials=self.__credentials,
            #        enabled=enabled,
            #        real_name=real_name,
            #        inactivity_timeout=None if inactivity_timeout == 0 else inactivity_timeout,
            #        ui_locale=ui_locale,
            #        email_addresses=email_addresses)
            self.__result = CreateActivityTypeDialogResult.CANCEL
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = CreateActivityTypeDialogResult.CANCEL
        self.end_modal()
