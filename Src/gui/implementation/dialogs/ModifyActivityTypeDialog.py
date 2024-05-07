""" Implements the "Modify activity type" modal dialog. """

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
class ModifyActivityTypeDialogResult(Enum):
    """ The result of modal invocation of the ModifyActivityTypeDialog. """

    OK = 1
    """ The BusinessActivityType has been modified. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class ModifyActivityTypeDialog(Dialog):
    """ The modal "Modify activity type" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 activity_type: BusinessActivityType = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Modify activity type" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param activity_type:
                The activity type to modify.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ModifyActivityTypeDialog.Title"))

        assert isinstance(activity_type, BusinessActivityType)
        self.__activity_type = activity_type
        self.__result = ModifyActivityTypeDialogResult.CANCEL

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None
        
        #   Save current user properties
        self.__activity_type_name = activity_type.get_name(self.__credentials)
        self.__activity_type_description = activity_type.get_description(self.__credentials)
        self.__validator = activity_type.workspace.validator

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyActivityTypeDialog.NameLabel.Text"),
            anchor=tk.E)
        self.__name_text_field = TextField(self.__controls_panel, width=40)

        self.__description_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyActivityTypeDialog.DescriptionLabel.Text"),
            anchor=tk.E)
        self.__description_text_area = TextArea(self.__controls_panel, height=4, width=40)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ModifyActivityTypeDialog.OkButton.Text"),
            image=GuiResources.image("ModifyActivityTypeDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("ModifyActivityTypeDialog.CancelButton.Text"),
            image=GuiResources.image("ModifyActivityTypeDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__description_text_area.accept_tab = False
        
        self.__name_text_field.text = self.__activity_type_name
        self.__description_text_area.text = self.__activity_type_description

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__description_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__description_text_area.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__name_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__description_text_area.add_property_change_listener(self.__text_field_change_listener)

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
            self.__validator.activity_type.is_valid_name(self.__name_text_field.text) and
            self.__validator.activity_type.is_valid_description(self.__description_text_area.text))

    ##########
    #   Properties
    @property
    def result(self) -> ModifyActivityTypeDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        name = self.__name_text_field.text.strip()
        description = self.__description_text_area.text.rstrip()
        
        try:
            if name != self.__activity_type_name:
                self.__activity_type.set_name(self.__credentials, name)
            if description != self.__activity_type_description:
                self.__activity_type.set_description(self.__credentials, description)
            self.__result = ModifyActivityTypeDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = ModifyActivityTypeDialogResult.CANCEL
        self.end_modal()
