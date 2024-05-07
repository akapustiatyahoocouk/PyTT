""" The message box modal dialog. """

#   Python standard library
from typing import final, TypeAlias, Callable
from enum import Enum
from inspect import signature
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent
from .Dialog import Dialog
from .Panel import Panel
from .Label import Label
from .TextField import TextField
from .Separator import Separator
from .Button import Button
from ..resources.AwtResources import AwtResources

##########
#   Public entities
@final
class EditStringDialogResult(Enum):
    """ The result of modal invocation of the EditStringDialog. """

    OK = 1
    """ User has confirmed the edited string. """

    CANCEL = 2
    """ Dialog cancelled by user. """

class EditStringDialog(Dialog):
    """ A modal dialog that allows the user to interactively edit a string. """

    ##########
    #   Types
    Validator: TypeAlias = Callable[[str], bool]

    ##########
    #   Construction
    def __init__(self,
                 parent: tk.BaseWidget,
                 title: str,
                 prompt: str,
                 value: str = "",
                 validator: Validator = None):
        Dialog.__init__(self, parent, title)

        assert isinstance(title, str)
        assert isinstance(prompt, str)
        assert isinstance(value, str)
        assert ((validator is None) or
                (isinstance(validator, Callable) and len(signature(validator).parameters) == 1))

        self.__value = value
        self.__validator = validator
        self.__result = EditStringDialogResult.CANCEL

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__prompt_label = Label(self.__controls_panel, text=prompt, anchor=tk.W)
        self.__value_text_field = TextField(self.__controls_panel, width=40, text=value)

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=AwtResources.string("EditStringDialog.OkButton.Text"),
            image=AwtResources.image("EditStringDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=AwtResources.string("EditStringDialog.CancelButton.Text"),
            image=AwtResources.image("EditStringDialog.CancelButton.Icon"))

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)

        self.__prompt_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__value_text_field.grid(row=1, column=0, padx=2, pady=2, sticky="WE")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)

        self.__cancel_button.pack(side=tk.RIGHT, padx=0, pady=0)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__value_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        if self.__validator is None:
            self.__ok_button.enabled = True
        else:
            self.__ok_button.enabled = self.__validator(self.__value_text_field.text) is True

    ##########
    #   Properties
    @property
    def result(self) -> EditStringDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def value(self) -> str:
        """ The string as edited by the user. """
        return self.__value

    ##########
    #   Operations

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_ok(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        self.__value = self.__value_text_field.text
        self.__result = EditStringDialogResult.OK
        self.end_modal()

    def __on_cancel(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        self.__result = EditStringDialogResult.CANCEL
        self.end_modal()
