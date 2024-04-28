""" Implements "Login to PyTT" modal dialog. """
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk
import traceback

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
class CreateWorkspaceDialog(Dialog):
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
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("CreateWorkspaceDialog.Title"))

        self.__result = CreateWorkspaceDialogResult.CANCEL
        self.__workspace = None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__workspace_type_label = Label(self.__controls_panel,
                                            text=GuiResources.string("CreateWorkspaceDialog.WorkspaceTypeLabel.Text"),
                                            anchor=tk.E)
        self.__workspace_type_combo_box = ComboBox(self.__controls_panel)

        self.__workspace_address_label = Label(self.__controls_panel,
                                               text=GuiResources.string("CreateWorkspaceDialog.WorkspaceAddressLabel.Text"),
                                               anchor=tk.E)
        self.__workspace_address_text_field = TextField(self.__controls_panel, width=40)
        self.__browse_button = Button(self.__controls_panel,
                                      text=GuiResources.string("CreateWorkspaceDialog.BrowseButton.Text"),
                                      image=GuiResources.image("CreateWorkspaceDialog.BrowseButton.Icon"))

        self.__radio_button_group = RadioButtonGroup()
        self.__use_current_credentials_radio_button = \
            RadioButton(self.__controls_panel,
                        self.__radio_button_group,
                        text=GuiResources.string("CreateWorkspaceDialog.UseCurrentCredentialsRadioButton.Text"))
        self.__use_custom_credentials_radio_button = \
            RadioButton(self.__controls_panel,
                        self.__radio_button_group,
                        text=GuiResources.string("CreateWorkspaceDialog.UseCustomCredentialsRadioButton.Text"))

        self.__admin_user_label = Label(self.__controls_panel,
                                        text=GuiResources.string("CreateWorkspaceDialog.AdminUserLabel.Text"),
                                        anchor=tk.E)
        self.__admin_user_text_field = TextField(self.__controls_panel, width=40)

        self.__admin_account_label = Label(self.__controls_panel,
                                           text=GuiResources.string("CreateWorkspaceDialog.AdminAccountLabel.Text"),
                                           anchor=tk.E)
        self.__admin_account_text_field = TextField(self.__controls_panel, width=40)

        self.__admin_password1_label = Label(self.__controls_panel,
                                            text=GuiResources.string("CreateWorkspaceDialog.AdminPassword1Label.Text"),
                                            anchor=tk.E)
        self.__admin_password1_text_field = TextField(self.__controls_panel, width=40)

        self.__admin_password2_label = Label(self.__controls_panel,
                                            text=GuiResources.string("CreateWorkspaceDialog.AdminPassword2Label.Text"),
                                            anchor=tk.E)
        self.__admin_password2_text_field = TextField(self.__controls_panel, width=40)

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

        self.__workspace_address_text_field.readonly = True

        self.__selected_workspace_type = self.__workspace_type_combo_box.selected_item
        self.__selected_workspace_address = None

        self.__use_current_credentials_radio_button.checked = True
        self.__admin_password1_text_field.password_entry = True
        self.__admin_password2_text_field.password_entry = True

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__workspace_type_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__workspace_type_combo_box.grid(row=0, column=1, columnspan=2, padx=2, pady=2, sticky="WE")

        self.__workspace_address_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__workspace_address_text_field.grid(row=1, column=1, padx=2, pady=2, sticky="WE")
        self.__browse_button.grid(row=1, column=2, padx=2, pady=2, sticky="E")

        self.__use_current_credentials_radio_button.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky="W")
        self.__use_custom_credentials_radio_button.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky="W")

        self.__admin_user_label.grid(row=4, column=0, padx=2, pady=2, sticky="W")
        self.__admin_user_text_field.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky="WE")
        self.__admin_account_label.grid(row=5, column=0, padx=2, pady=2, sticky="W")
        self.__admin_account_text_field.grid(row=5, column=1, columnspan=2, padx=2, pady=2, sticky="WE")
        self.__admin_password1_label.grid(row=6, column=0, padx=2, pady=2, sticky="W")
        self.__admin_password1_text_field.grid(row=6, column=1, columnspan=2, padx=2, pady=2, sticky="WE")
        self.__admin_password2_label.grid(row=7, column=0, padx=2, pady=2, sticky="W")
        self.__admin_password2_text_field.grid(row=7, column=1, columnspan=2, padx=2, pady=2, sticky="WE")
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__workspace_type_combo_box.add_item_listener(self.__on_workspace_type_changed)
        self.__browse_button.add_action_listener(self.__on_browse)

        self.__use_current_credentials_radio_button.add_action_listener(self.__on_admin_mode_changed)
        self.__use_custom_credentials_radio_button.add_action_listener(self.__on_admin_mode_changed)
        
        self.__admin_user_text_field.add_property_change_listener(self.__on_custom_credentials_changed)
        self.__admin_account_text_field.add_property_change_listener(self.__on_custom_credentials_changed)
        self.__admin_password1_text_field.add_property_change_listener(self.__on_custom_credentials_changed)
        self.__admin_password2_text_field.add_property_change_listener(self.__on_custom_credentials_changed)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__workspace_address_label.enabled = self.__selected_workspace_type is not None
        self.__browse_button.enabled = self.__selected_workspace_type is not None

        custom_admin_credentials = self.__use_custom_credentials_radio_button.checked
        self.__admin_user_label.enabled = custom_admin_credentials
        self.__admin_user_text_field.enabled = custom_admin_credentials
        self.__admin_account_label.enabled = custom_admin_credentials
        self.__admin_account_text_field.enabled = custom_admin_credentials
        self.__admin_password1_label.enabled = custom_admin_credentials
        self.__admin_password1_text_field.enabled = custom_admin_credentials
        self.__admin_password2_label.enabled = custom_admin_credentials
        self.__admin_password2_text_field.enabled = custom_admin_credentials
        credentials_valid = (True if not custom_admin_credentials
                             else len(self.__admin_user_text_field.text.strip()) > 0 and
                                  len(self.__admin_account_text_field.text.strip()) > 0 and
                                  self.__admin_password1_text_field.text == self.__admin_password2_text_field.text)
                             

        self.__ok_button.enabled = (self.__selected_workspace_address is not None) and credentials_valid

    ##########
    #   Properties
    @property
    def result(self) -> CreateWorkspaceDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def created_workspace(self) -> Workspace:
        """ The workspace created by the user; None if the
            user has cancelled the dialog. """
        return self.__workspace

    ##########
    #   Event listeners
    def __on_workspace_type_changed(self, evt: ItemEvent) -> None:
        wt = self.__workspace_type_combo_box.selected_item
        if wt != self.__selected_workspace_type:
            self.__selected_workspace_type = wt
            self.__selected_workspace_address = None
            self.__workspace_address_text_field.text = ""
            self.request_refresh()

    def __on_browse(self, evt: ActionEvent) -> None:
        wa = self.__selected_workspace_type.enter_new_workspace_address(self)
        if wa is None:
            return
        self.__selected_workspace_address = wa
        self.__workspace_address_text_field.text = wa.display_form
        self.request_refresh()

    def __on_admin_mode_changed(self, evt: ActionEvent) -> None:
        self.request_refresh()

    def __on_custom_credentials_changed(self, evt: PropertyChangeEvent) -> None:
        self.request_refresh()

    def __on_ok(self, evt: ActionEvent) -> None:
        if not self.__ok_button.enabled:
            return
        try:
            if self.__use_custom_credentials_radio_button.checked:
                user = self.__admin_user_text_field.text.strip()
                login = self.__admin_account_text_field.text.strip()
                password = self.__admin_password1_text_field.text
            else:
                user = CurrentCredentials.get().login
                login = CurrentCredentials.get().login
                password = CurrentCredentials.get()._Credentials__password
            self.__workspace = self.__selected_workspace_type.create_workspace(
                address=self.__selected_workspace_address,
                admin_user=user,
                admin_login=login,
                admin_password=password)
            self.__result = CreateWorkspaceDialogResult.OK
            CurrentCredentials.set(Credentials(login, password))
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt: ActionEvent) -> None:
        self.__result = CreateWorkspaceDialogResult.CANCEL
        self.end_modal()
