""" Implements "Manage public tasks" modal dialog. """

#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from ..views.PublicTasksView import PublicTasksView
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class ManagePublicTasksDialogResult(Enum):  #   TODO do we even need it ?
    """ The result of modal invocation of the ManagePublicTasksDialog. """

    OK = 1
    """ User has closed the dialog. """

@final
class ManagePublicTasksDialog(Dialog):
    """ The modal "Manage public tasks" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        """
            Constructs the "Manage public tasks" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ManagePublicTasksDialog.Title"))

        self.__result = ManagePublicTasksDialogResult.OK

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__public_tasks_view = PublicTasksView(self.__controls_panel)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ManagePublicTasksDialog.OkButton.Text"),
            image=GuiResources.image("ManagePublicTasksDialog.OkButton.Icon"))

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)

        self.__public_tasks_view.grid(row=0, column=1, padx=2, pady=2, sticky="NSWE")

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
    def result(self) -> ManagePublicTasksDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __on_ok(self, evt = None) -> None:
        self.__result = ManagePublicTasksDialogResult.OK
        self.end_modal()


