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
from ..controls.EmailAddressListEditor import EmailAddressListEditor

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

        self.__real_name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateUserDialog.RealNameLabel.Text"),
            anchor=tk.E)
        self.__real_name_text_field = TextField(self.__controls_panel, width=40)

        self.__enabled_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("CreateUserDialog.EnabledCheckBox.Text"))

        self.__email_addresses_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateUserDialog.EmailAddressesLabel.Text"),
            anchor=tk.E)
        self.__email_address_list_editor = EmailAddressListEditor(self.__controls_panel)

        self.__inactivity_timeout_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateUserDialog.InactivityTimeoutLabel.Text"),
            anchor=tk.E)
        self.__inactivity_timeout_panel = Panel(self.__controls_panel)
        self.__inactivity_timeout_value_combo_box = ComboBox(self.__inactivity_timeout_panel)
        self.__inactivity_timeout_unit_combo_box = ComboBox(self.__inactivity_timeout_panel)

        self.__ui_locale_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreateUserDialog.UiLocaleLabel.Text"),
            anchor=tk.E)
        self.__ui_locale_combo_box = ComboBox(self.__controls_panel)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreateUserDialog.OkButton.Text"),
            image=GuiResources.image("CreateUserDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreateUserDialog.CancelButton.Text"),
            image=GuiResources.image("CreateUserDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__enabled_check_box.checked = True
        
        for i in range(60):
            if i == 0:
                self.__inactivity_timeout_value_combo_box.items.add(
                    GuiResources.string("CreateUserDialog.InactivityTimeoutNone"),
                    tag=i)
            else:
                self.__inactivity_timeout_value_combo_box.items.add(str(i), tag=i)
        self.__inactivity_timeout_value_combo_box.selected_index = 1
        self.__inactivity_timeout_value_combo_box.editable = False

        self.__inactivity_timeout_unit_combo_box.items.add(
            GuiResources.string("CreateUserDialog.InactivityTimeoutMinutes"),
            tag=1)
        self.__inactivity_timeout_unit_combo_box.items.add(
            GuiResources.string("CreateUserDialog.InactivityTimeoutHours"),
            tag=60)
        self.__inactivity_timeout_unit_combo_box.selected_index = 1
        self.__inactivity_timeout_unit_combo_box.editable = False

        all_locales = list(LocalizableSubsystem.all_supported_locales())
        all_locales.sort(key=lambda l: repr(l))
        self.__ui_locale_combo_box.items.add(
            GuiResources.string("CreateUserDialog.UiLocaleSystemDefault"),
            tag=None)
        for locale in all_locales:
            self.__ui_locale_combo_box.items.add(str(locale), tag=locale)
        self.__ui_locale_combo_box.selected_index = 0
        self.__ui_locale_combo_box.editable = False

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__real_name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__real_name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__enabled_check_box.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__email_addresses_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.__email_address_list_editor.grid(row=2, column=1, padx=2, pady=2, sticky="WE")

        self.__inactivity_timeout_label.grid(row=3, column=0, padx=2, pady=2, sticky="W")
        self.__inactivity_timeout_panel.grid(row=3, column=1, padx=0, pady=0, sticky="W")
        self.__inactivity_timeout_value_combo_box.pack(side=tk.LEFT, padx=2, pady=2)
        self.__inactivity_timeout_unit_combo_box.pack(side=tk.LEFT, padx=2, pady=2)

        self.__ui_locale_label.grid(row=4, column=0, padx=2, pady=2, sticky="W")
        self.__ui_locale_combo_box.grid(row=4, column=1, padx=2, pady=2, sticky="W")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__real_name_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__inactivity_timeout_value_combo_box.add_item_listener(self.__combo_box_listener)
        self.__inactivity_timeout_unit_combo_box.add_item_listener(self.__combo_box_listener)
        self.__ui_locale_combo_box.add_item_listener(self.__combo_box_listener)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__inactivity_timeout_unit_combo_box.enabled = \
            ((self.__inactivity_timeout_value_combo_box.selected_item is not None) and
             (self.__inactivity_timeout_value_combo_box.selected_item.tag != 0))
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
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __combo_box_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        real_name = self.__real_name_text_field.text
        enabled = self.__enabled_check_box.checked
        ui_locale = self.__ui_locale_combo_box.selected_item.tag
        inactivity_timeout = (self.__inactivity_timeout_value_combo_box.selected_item.tag *
                              self.__inactivity_timeout_unit_combo_box.selected_item.tag)
        email_addresses = self.__email_address_list_editor.email_addresses
        
        try:
            self.__created_user = self.__workspace.create_user(
                    credentials=self.__credentials,
                    enabled=enabled,
                    real_name=real_name,
                    inactivity_timeout=None if inactivity_timeout == 0 else inactivity_timeout,
                    ui_locale=ui_locale,
                    email_addresses=email_addresses)
            self.__result = CreateUserDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = CreateUserDialogResult.CANCEL
        self.end_modal()
