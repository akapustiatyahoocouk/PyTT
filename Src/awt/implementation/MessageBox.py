"""
    The message box modal dialog.
"""
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk
from turtle import bgcolor
from typing import Any
from enum import Enum

from .ActionEvent import ActionEvent

#   Internal dependencies on modules within the same component
from .Dialog import Dialog
from .Panel import Panel
from .Label import Label
from .Separator import Separator
from .Button import Button
from awt.resources.AwtResources import AwtResources

##########
#   Public entities
class MessageBoxIcon(Enum):
    NONE = 0
    INFORMATION = 1
    QUESTION = 2
    ERROR = 3

class MessageBoxButtons(Enum):
    OK = 1
    OK_CANCEL = 2
    YES_NO = 3
    YES_NO_CANCEL = 4
    ABORT_RETRY_IGNORE = 5
    CANCEL_RETRY_CONTINUE = 6
    RETRY_CANCEL = 7

class MessageBoxResult(Enum):
    NONE = 0
    OK = 1
    CANCEL = 2
    YES = 3
    NO = 4
    ABORT = 5
    RETRY = 6
    IGNORE = 7
    CONTINUE = 8

class MessageBox(Dialog):

    ##########
    #   Construction
    def __init__(self,
                 parent: tk.BaseWidget,
                 title: str, 
                 message: str,
                 icon: MessageBoxIcon = MessageBoxIcon.NONE,
                 buttons: MessageBoxButtons = MessageBoxButtons.OK):
        Dialog.__init__(self, parent, title)

        assert isinstance(title, str)
        assert isinstance(message, str)
        assert isinstance(icon, MessageBoxIcon)
        assert isinstance(buttons, MessageBoxButtons)

        self.__result = MessageBoxResult.NONE

        #   Create controls
        self.__controls_panel = Panel(self)
        self.__pan1 = Panel(self.__controls_panel)
        self.__pan2 = Panel(self.__controls_panel)

        match icon:
            case MessageBoxIcon.NONE:
                self.__pic1 = Label(self.__pan1)
            case MessageBoxIcon.INFORMATION:
                self.__pic1 = Label(self.__pan1, image = AwtResources.image("MessageBox.InformationIcon"))
            case MessageBoxIcon.QUESTION:
                self.__pic1 = Label(self.__pan1, image = AwtResources.image("MessageBox.QuestionIcon"))
            case MessageBoxIcon.ERROR:
                self.__pic1 = Label(self.__pan1, image = AwtResources.image("MessageBox.ErrorIcon"))
        self.__text = Label(self.__pan2, text=str(message))

        self.__separator = Separator(self, orient="horizontal")

        match buttons:
            case MessageBoxButtons.OK:
                self.__ok_button = Button(self,
                    text=AwtResources.string("MessageBox.OkButton.Text"),
                    image=AwtResources.image("MessageBox.OkButton.Icon"))
            case MessageBoxButtons.OK_CANCEL:
                self.__ok_button = Button(self,
                    text=AwtResources.string("MessageBox.OkButton.Text"),
                    image=AwtResources.image("MessageBox.OkButton.Icon"))
                self.__cancel_button = Button(self,
                    text=AwtResources.string("MessageBox.CancelButton.Text"),
                    image=AwtResources.image("MessageBox.CancelButton.Icon"))
            case _:
                raise NotImplementedError()

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__pan1.pack(side=tk.LEFT, padx=0, pady=0)
        self.__pan2.pack(fill=tk.X, padx=0, pady=0)

        self.__pic1.pack(fill=tk.NONE, padx=2, pady=2)
        self.__text.pack(fill=tk.X, padx=2, pady=2)

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        match buttons:
            case MessageBoxButtons.OK:
                self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)
            case MessageBoxButtons.OK_CANCEL:
                self.__cancel_button.pack(side=tk.RIGHT, padx=0, pady=0)
                self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)
            case _:
                raise NotImplementedError()

        #   Set up event handlers
        match buttons:
            case MessageBoxButtons.OK:
                self.ok_button = self.__ok_button
                self.cancel_button = self.__ok_button
                self.__ok_button.add_action_listener(self.__on_ok)
            case MessageBoxButtons.OK_CANCEL:
                self.ok_button = self.__ok_button
                self.cancel_button = self.__cancel_button
                self.__ok_button.add_action_listener(self.__on_ok)
                self.__cancel_button.add_action_listener(self.__on_cancel)
            case _:
                raise NotImplementedError()

        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Operations
    @staticmethod
    def show(parent: tk.BaseWidget,
             title: str, 
             message: str,
             icon: MessageBoxIcon = MessageBoxIcon.NONE,
             buttons: MessageBoxButtons = MessageBoxButtons.OK):
        with MessageBox(parent, title, message, icon, buttons) as mb:
            mb.do_modal()

    ##########
    #   Event listeners
    def __on_ok(self, evt: ActionEvent) -> None:
        self.__result = MessageBoxResult.OK
        self.end_modal()

    def __on_cancel(self, evt: ActionEvent) -> None:
        self.__result = MessageBoxResult.CANCEL
        self.end_modal()
