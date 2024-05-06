""" Implements the "Destroy account" modal dialog. """

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
class DestroyAccountDialogResult(Enum):
    """ The result of modal invocation of the DestroyAccountDialog. """

    OK = 1
    """ A BusinessAccount has been destroyed. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class DestroyAccountDialog(Dialog):
    """ The modal "Destroy account" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 account: BusinessAccount = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Destroy account" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param account:
                The BusinessAccount to destroy.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("DestroyAccountDialog.Title"))

        assert isinstance(account, BusinessAccount)
        self.__account = account
        self.__result = DestroyAccountDialogResult.CANCEL

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__prompt_label = Label(
            self.__controls_panel,
            text=GuiResources.string("DestroyAccountDialog.PrimptLabel.Text").format(account.display_name,
                                                                                     account.get_user(self.__credentials).display_name),
            justify=tk.CENTER)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("DestroyAccountDialog.OkButton.Text"),
            image=GuiResources.image("DestroyAccountDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("DestroyAccountDialog.CancelButton.Text"),
            image=GuiResources.image("DestroyAccountDialog.CancelButton.Icon"))

        #   Adjust controls

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)

        self.__prompt_label.grid(row=0, column=0, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Properties
    @property
    def result(self) -> DestroyAccountDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __on_ok(self, evt = None) -> None:
        try:
            self.__account.destroy(self.__credentials)
            self.__result = DestroyAccountDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = DestroyAccountDialogResult.CANCEL
        self.end_modal()


