""" Implements the "Destroy activity type" modal dialog. """

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
class DestroyActivityTypeDialogResult(Enum):
    """ The result of modal invocation of the DestroyActivityTypeDialog. """

    OK = 1
    """ A BusinessActivityType has been destroyed. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class DestroyActivityTypeDialog(Dialog):
    """ The modal "Destroy activity type" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 activity_type: BusinessActivityType = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Destroy activity type" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param activity_type:
                The BusinessActivityType to destroy.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("DestroyActivityTypeDialog.Title"))

        assert isinstance(activity_type, BusinessActivityType)
        self.__activity_type = activity_type
        self.__result = DestroyActivityTypeDialogResult.CANCEL

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__prompt_label = Label(
            self.__controls_panel,
            text=GuiResources.string("DestroyActivityTypeDialog.PrimptLabel.Text").format(activity_type.display_name),
            justify=tk.CENTER)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("DestroyActivityTypeDialog.OkButton.Text"),
            image=GuiResources.image("DestroyActivityTypeDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("DestroyActivityTypeDialog.CancelButton.Text"),
            image=GuiResources.image("DestroyActivityTypeDialog.CancelButton.Icon"))

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
    def result(self) -> DestroyActivityTypeDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __on_ok(self, evt = None) -> None:
        try:
            self.__activity_type.destroy(self.__credentials)
            self.__result = DestroyActivityTypeDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = DestroyActivityTypeDialogResult.CANCEL
        self.end_modal()


