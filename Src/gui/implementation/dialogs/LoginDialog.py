"""
    Implements "Login to PyTT" modal dialog.
"""
#   Python standard library
from typing import Self, final, Optional, Callable
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

        self.__result = LoginDialogResult.CANCEL
        self.__credentials = None

        #   Create control models
        self.__login_var = tk.StringVar(value=login)
        self.__password_var = tk.StringVar()

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__login_label = Label(self.__controls_panel,
                                   text=GuiResources.string("LoginDialog.LoginLabel.Text"),
                                   anchor=tk.E)
        self.__login_text_field = TextField(self.__controls_panel, width=40, textvariable=self.__login_var)

        self.__password_label = Label(self.__controls_panel,
                                      text=GuiResources.string("LoginDialog.PasswordLabel.Text"),
                                      anchor=tk.E)
        self.__password_text_field = TextField(self.__controls_panel, width=40, show="\u2022", textvariable=self.__password_var)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("LoginDialog.OkButton.Text"),
            image=GuiResources.image("LoginDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("LoginDialog.CancelButton.Text"),
            image=GuiResources.image("LoginDialog.CancelButton.Icon"))

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

        self.__login_var.trace_add("write", lambda x,y,z: self.request_refresh())
        self.__password_var.trace_add("write", lambda x,y,z: self.request_refresh())

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Set initial focus & we're done
        if login is not None:
            self.__password_text_field.focus_set()
        else:
            self.__login_text_field.focus_set()
        self.request_refresh()

        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        login: str = self.__login_var.get()
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
        return self.__login_text_field if len(self.__login_var.get()) == 0 else self.__password_text_field

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
    def __on_ok(self, evt = None) -> None:
        if not self.__ok_button.enabled:
            return
        login = self.__login_var.get()
        password = self.__password_var.get()
        self.__credentials = Credentials(login, password)
        self.__result = LoginDialogResult.OK
        self.end_modal()

    def __on_cancel(self, evt = None) -> None:
        self.__credentials = None
        self.__result = LoginDialogResult.CANCEL
        self.end_modal()
