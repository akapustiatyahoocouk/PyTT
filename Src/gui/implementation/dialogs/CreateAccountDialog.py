""" Implements the "Create" modal dialog. """

#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

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
class CreateAccountDialogResult(Enum):
    """ The result of modal invocation of the CreateAccountDialog. """

    OK = 1
    """ A BusinessAccount has been created. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class CreateAccountDialog(Dialog):
    """ The modal "Create account" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 user: BusinessUser = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Create Account" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param user:
                The BusinessUser to create a BusinessAccount for.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("CreateAccountDialog.Title"))

        assert isinstance(user, BusinessUser)
        self.__user = user
        self.__result = CreateAccountDialogResult.CANCEL
        self.__created_account = None

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__login_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.LoginLabel.Text"),
            anchor=tk.E)
        self.__login_text_field = TextField(
            self.__controls_panel,
            width=40)

        self.__password1_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.Password1Label.Text"),
            anchor=tk.E)
        self.__password1_text_field = TextField(
            self.__controls_panel,
            width=40)

        self.__password2_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.Password2Label.Text"),
            anchor=tk.E)
        self.__password2_text_field = TextField(
            self.__controls_panel,
            width=40)

        self.__enabled_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.EnabledCheckBox.Text"))

        self.__email_addresses_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.EmailAddressesLabel.Text"),
            anchor=tk.E)
        self.__email_address_list_editor = EmailAddressListEditor(self.__controls_panel)

        self.__capabilities_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateAccountDialog.CapabilitiesLabel.Text"),
            anchor=tk.E)
        self.__capabilities_panel = Panel(self.__controls_panel)

        self.__administrator_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.ADMINISTRATOR))
        self.__manage_users_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_USERS))
        self.__manage_stock_items_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_STOCK_ITEMS))
        self.__manage_beneficiaries_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_BENEFICIARIES))
        self.__manage_workloads_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_WORKLOADS))
        self.__manage_public_activities_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_PUBLIC_ACTIVITIES))
        self.__manage_public_tasks_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_PUBLIC_TASKS))
        self.__manage_private_activities_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_PRIVATE_ACTIVITIES))
        self.__manage_private_tasks_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.MANAGE_PRIVATE_TASKS))
        self.__log_work_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.LOG_WORK))
        self.__log_events_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.LOG_EVENTS))
        self.__generate_reports_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.GENERATE_REPORTS))
        self.__backup_and_restore_check_box = CheckBox(
            self.__capabilities_panel,
            text=str(Capability.BACKUP_AND_RESTORE))

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreateAccountDialog.OkButton.Text"),
            image=GuiResources.image("CreateAccountDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreateAccountDialog.CancelButton.Text"),
            image=GuiResources.image("CreateAccountDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__enabled_check_box.checked = True
        self.__password1_text_field.password_entry = True
        self.__password2_text_field.password_entry = True
        self.__log_work_check_box.checked = True
        self.__log_events_check_box.checked = True

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__login_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__login_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__password1_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__password1_text_field.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__password2_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.__password2_text_field.grid(row=2, column=1, padx=2, pady=2, sticky="WE")

        self.__enabled_check_box.grid(row=3, column=1, padx=2, pady=2, sticky="WE")

        self.__email_addresses_label.grid(row=4, column=0, padx=2, pady=2, sticky="W")
        self.__email_address_list_editor.grid(row=4, column=1, padx=2, pady=2, sticky="WE")

        self.__capabilities_label.grid(row=5, column=0, padx=2, pady=2, sticky="W")
        self.__capabilities_panel.grid(row=5, column=1, padx=2, pady=2, sticky="WE")
        self.__administrator_check_box.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__manage_users_check_box.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__manage_stock_items_check_box.grid(row=1, column=1, padx=2, pady=2, sticky="W")
        self.__manage_beneficiaries_check_box.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.__manage_workloads_check_box.grid(row=2, column=1, padx=2, pady=2, sticky="W")
        self.__manage_public_activities_check_box.grid(row=3, column=0, padx=2, pady=2, sticky="W")
        self.__manage_public_tasks_check_box.grid(row=3, column=1, padx=2, pady=2, sticky="W")
        self.__manage_private_activities_check_box.grid(row=4, column=0, padx=2, pady=2, sticky="W")
        self.__manage_private_tasks_check_box.grid(row=4, column=1, padx=2, pady=2, sticky="W")
        self.__log_work_check_box.grid(row=5, column=0, padx=2, pady=2, sticky="W")
        self.__log_events_check_box.grid(row=5, column=1, padx=2, pady=2, sticky="W")
        self.__generate_reports_check_box.grid(row=6, column=0, padx=2, pady=2, sticky="W")
        self.__backup_and_restore_check_box.grid(row=6, column=1, padx=2, pady=2, sticky="W")
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__login_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__password1_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__password2_text_field.add_property_change_listener(self.__text_field_change_listener)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__ok_button.enabled = (
            (len(self.__login_text_field.text.strip()) > 0) and
            (self.__password1_text_field.text == self.__password2_text_field.text))

    ##########
    #   Properties
    @property
    def result(self) -> CreateAccountDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def created_account(self) -> Optional[BusinessAccount]:
        """ The BusinessAccount created during dialog invocation;
            None if the dialog was cancelled. """
        return self.__created_account

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        login = self.__login_text_field.text
        password = self.__password1_text_field.text
        enabled = self.__enabled_check_box.checked
        email_addresses = self.__email_address_list_editor.email_addresses
        capabilities = Capabilities.NONE
        if self.__administrator_check_box.checked:
            capabilities |= Capabilities.ADMINISTRATOR
        if self.__manage_users_check_box.checked:
            capabilities |= Capabilities.MANAGE_USERS
        if self.__manage_stock_items_check_box.checked:
            capabilities |= Capabilities.MANAGE_STOCK_ITEMS
        if self.__manage_beneficiaries_check_box.checked:
            capabilities |= Capabilities.MANAGE_BENEFICIARIES
        if self.__manage_workloads_check_box.checked:
            capabilities |= Capabilities.MANAGE_WORKLOADS
        if self.__manage_public_activities_check_box.checked:
            capabilities |= Capabilities.MANAGE_PUBLIC_ACTIVITIES
        if self.__manage_public_tasks_check_box.checked:
            capabilities |= Capabilities.MANAGE_PUBLIC_TASKS
        if self.__manage_private_activities_check_box.checked:
            capabilities |= Capabilities.MANAGE_PRIVATE_ACTIVITIES
        if self.__manage_private_tasks_check_box.checked:
            capabilities |= Capabilities.MANAGE_PRIVATE_TASKS
        if self.__log_work_check_box.checked:
            capabilities |= Capabilities.LOG_WORK
        if self.__log_events_check_box.checked:
            capabilities |= Capabilities.LOG_EVENTS
        if self.__generate_reports_check_box.checked:
            capabilities |= Capabilities.GENERATE_REPORTS
        if self.__backup_and_restore_check_box.checked:
            capabilities |= Capabilities.BACKUP_AND_RESTORE

        try:
            self.__created_account = self.__user.create_account(
                    credentials=self.__credentials,
                    enabled=enabled,
                    login=login,
                    password=password,
                    capabilities=capabilities,
                    email_addresses=email_addresses)
            self.__result = CreateAccountDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)
    
    def __on_cancel(self, evt = None) -> None:
        self.__result = CreateAccountDialogResult.CANCEL
        self.end_modal()
