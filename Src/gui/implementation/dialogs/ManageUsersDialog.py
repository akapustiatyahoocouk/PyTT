""" Implements "Manage users" modal dialog. """
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..views.UsersView import UsersView
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class ManageUsersDialogResult(Enum):  #   TODO do we even need it ?
    """ The result of modal invocation of the ManageUsersDialog. """

    OK = 1
    """ User has closed the dialog. """

@final
class ManageUsersDialog(Dialog):
    """ The modal "Manage users" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        """
            Constructs the "Manage users" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ManageUsersDialog.Title"))

        self.__result = ManageUsersDialogResult.OK

        #   Create controls
        self.__users_view = UsersView(self)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ManageUsersDialog.OkButton.Text"),
            image=GuiResources.image("ManageUsersDialog.OkButton.Icon"))

        #   Set up control structure
        self.__users_view.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__ok_button

        self.__ok_button.add_action_listener(self.__on_ok)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Properties
    @property
    def result(self) -> ManageUsersDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __on_ok(self, evt = None) -> None:
        self.__result = ManageUsersDialogResult.OK
        self.end_modal()
