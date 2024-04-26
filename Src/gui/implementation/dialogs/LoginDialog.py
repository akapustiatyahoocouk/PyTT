""" Implements "Login to PyTT" modal dialog. """
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources
from ..misc.GuiSettings import GuiSettings

##########
#   Public entities
@final
class LoginDialogResult(Enum):
    """ The result of modal invocation of the LoginDialog. """

    OK = 1
    """ User has supplied the login details. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class LoginDialog(Dialog):
    """ The modal "login" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, login: Optional[str] = None):
        """
            Constructs the login dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param login:
                The login identifier to initially display in the "login"
                field or None. If spefified, the initial keyboard focus
                goes straight to the "password" field.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("LoginDialog.Title"))

        login = login if isinstance(login, str) else ""
        self.__result = LoginDialogResult.CANCEL
        self.__credentials = None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__login_label = Label(self.__controls_panel,
                                   text=GuiResources.string("LoginDialog.LoginLabel.Text"),
                                   anchor=tk.E)
        self.__login_text_field = TextField(self.__controls_panel, width=40, text=login)

        self.__password_label = Label(self.__controls_panel,
                                      text=GuiResources.string("LoginDialog.PasswordLabel.Text"),
                                      anchor=tk.E)
        self.__password_text_field = TextField(self.__controls_panel, width=40, text="")

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("LoginDialog.OkButton.Text"),
            image=GuiResources.image("LoginDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("LoginDialog.CancelButton.Text"),
            image=GuiResources.image("LoginDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__password_text_field.password_entry = True
        
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__login_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__login_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__password_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__password_text_field.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__login_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__password_text_field.add_property_change_listener(self.__text_field_change_listener)
                                                                
        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        login: str = self.__login_text_field.text
        if len(login.strip()) == 0:
            self.__password_label.enabled = False
            self.__password_text_field.enabled = False
            self.__ok_button.enabled = False
        else:
            self.__password_label.enabled = True
            self.__password_text_field.enabled = True
            self.__ok_button.enabled = True

    ##########
    #   Dialog
    @property
    def initial_focus(self) -> tk.BaseWidget:
        return self.__login_text_field if len(self.__login_text_field.text) == 0 else self.__password_text_field

    ##########
    #   Properties
    @property
    def result(self) -> LoginDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def credentials(self) -> Optional[Credentials]:
        """ The entered user credentials or None if the dialog
            was cancelled by the user. """
        return self.__credentials

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        if not self.__ok_button.enabled:
            return
        login = self.__login_text_field.text.strip()
        password = self.__password_text_field.text
        self.__credentials = Credentials(login, password)
        self.__result = LoginDialogResult.OK
        GuiSettings.last_login = login
        self.end_modal()

    def __on_cancel(self, evt = None) -> None:
        self.__credentials = None
        self.__result = LoginDialogResult.CANCEL
        self.end_modal()
