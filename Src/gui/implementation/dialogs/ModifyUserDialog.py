""" Implements the "Modify user" modal dialog. """

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
class ModifyUserDialogResult(Enum):
    """ The result of modal invocation of the ModifyUserDialog. """

    OK = 1
    """ A BusinessUser has been modified. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class ModifyUserDialog(Dialog):
    """ The modal "Modify user" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 user: BusinessUser = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Modify user" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param user:
                The BusinessUser to modify.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ModifyUserDialog.Title"))

        assert isinstance(user, BusinessUser)
        self.__user = user
        self.__result = ModifyUserDialogResult.CANCEL

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Save current user properties
        self.__user_enabled = user.is_enabled(self.__credentials)
        self.__user_real_name = user.get_real_name(self.__credentials)
        self.__user_inactivity_timeout = user.get_inactivity_timeout(self.__credentials)
        self.__user_ui_locale = user.get_ui_locale(self.__credentials)
        self.__user_email_addresses = user.get_email_addresses(self.__credentials)

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__real_name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyUserDialog.RealNameLabel.Text"),
            anchor=tk.E)
        self.__real_name_text_field = TextField(
            self.__controls_panel,
            width=40,
            text=self.__user_real_name)

        self.__enabled_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyUserDialog.EnabledCheckBox.Text"))

        self.__email_addresses_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyUserDialog.EmailAddressesLabel.Text"),
            anchor=tk.E)
        self.__email_address_list_editor = EmailAddressListEditor(self.__controls_panel)

        self.__inactivity_timeout_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyUserDialog.InactivityTimeoutLabel.Text"),
            anchor=tk.E)
        self.__inactivity_timeout_panel = Panel(self.__controls_panel)
        self.__inactivity_timeout_value_combo_box = ComboBox(self.__inactivity_timeout_panel)
        self.__inactivity_timeout_unit_combo_box = ComboBox(self.__inactivity_timeout_panel)

        self.__ui_locale_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyUserDialog.UiLocaleLabel.Text"),
            anchor=tk.E)
        self.__ui_locale_combo_box = ComboBox(self.__controls_panel)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ModifyUserDialog.OkButton.Text"),
            image=GuiResources.image("ModifyUserDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("ModifyUserDialog.CancelButton.Text"),
            image=GuiResources.image("ModifyUserDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__enabled_check_box.checked = self.__user_enabled

        self.__email_address_list_editor.email_addresses = self.__user_email_addresses

        for i in range(60):
            if i == 0:
                self.__inactivity_timeout_value_combo_box.items.add(
                    GuiResources.string("ModifyUserDialog.InactivityTimeoutNone"),
                    tag=i)
            else:
                self.__inactivity_timeout_value_combo_box.items.add(str(i), tag=i)
        self.__inactivity_timeout_value_combo_box.editable = False

        self.__inactivity_timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyUserDialog.InactivityTimeoutMinutes"),
            tag=1)
        self.__inactivity_timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyUserDialog.InactivityTimeoutHours"),
            tag=60)
        self.__inactivity_timeout_unit_combo_box.editable = False

        if self.__user_inactivity_timeout is None:
            self.__inactivity_timeout_value_combo_box.selected_index = 0
            self.__inactivity_timeout_unit_combo_box.selected_index = 1
        elif (self.__user_inactivity_timeout > 0 and
              self.__user_inactivity_timeout < 60):
            self.__inactivity_timeout_value_combo_box.selected_index = self.__user_inactivity_timeout
            self.__inactivity_timeout_unit_combo_box.selected_index = 0
        elif (self.__user_inactivity_timeout % 60 == 0 and
              self.__user_inactivity_timeout // 60 > 0 and
              self.__user_inactivity_timeout // 60 <= 60):
            self.__inactivity_timeout_value_combo_box.selected_index = self.__user_inactivity_timeout // 60
            self.__inactivity_timeout_unit_combo_box.selected_index = 1
        else:
            self.__inactivity_timeout_value_combo_box.selected_index = 1
            self.__inactivity_timeout_unit_combo_box.selected_index = 1

        all_locales = list(LocalizableSubsystem.all_supported_locales())
        all_locales.sort(key=lambda l: repr(l))
        self.__ui_locale_combo_box.items.add(
            GuiResources.string("ModifyUserDialog.UiLocaleSystemDefault"),
            tag=None)
        for locale in all_locales:
            self.__ui_locale_combo_box.items.add(str(locale), tag=locale)
        self.__ui_locale_combo_box.editable = False

        if self.__user_ui_locale in all_locales:
            self.__ui_locale_combo_box.selected_index = all_locales.index(self.__user_ui_locale) + 1
        else:
            self.__ui_locale_combo_box.selected_index = 0

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
    def result(self) -> ModifyUserDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

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
            #   Apply user properties (only those which have  changed)
            if enabled != self.__user_enabled:
                self.__user.set_enabled(self.__credentials, enabled);
            if real_name != self.__user_real_name:
                self.__user.set_real_name(self.__credentials, real_name);
            if inactivity_timeout != self.__user_inactivity_timeout:
                self.__user.set_inactivity_timeout(self.__credentials, inactivity_timeout);
            if ui_locale != self.__user_ui_locale:
                self.__user.set_ui_locale(self.__credentials, ui_locale);
            if email_addresses != self.__user_email_addresses:
                self.__user.set_email_addresses(self.__credentials, email_addresses);
            self.__result = ModifyUserDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = ModifyUserDialogResult.CANCEL
        self.end_modal()
