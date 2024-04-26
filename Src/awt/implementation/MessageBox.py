"""
    The message box modal dialog.
"""
#   Python standard library
import tkinter as tk
from enum import Enum

#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent
from .Dialog import Dialog
from .Panel import Panel
from .Label import Label
from .Separator import Separator
from .Button import Button
from ..resources.AwtResources import AwtResources

##########
#   Public entities
class MessageBoxIcon(Enum):
    """ The icons that a MessageBox can display. """

    NONE = 0
    """ No icon. """

    INFORMATION = 1
    """ An "information" icon (platform-specific). """

    QUESTION = 2
    """ A "question" icon (platform-specific). """

    ERROR = 3
    """ An "error" icon (platform-specific). """

class MessageBoxButtons(Enum):
    """ The sets of buttons a MessageBox can display. """

    OK = 1
    """ "OK" button. """

    OK_CANCEL = 2
    """ "OK" and "Cancel" buttons. """

    YES_NO = 3
    """ "Yes" and "No" buttons. """

    YES_NO_CANCEL = 4
    """ "Yes", "No" and "Cancel" buttons. """

    ABORT_RETRY_IGNORE = 5
    """ "Abort", "Retry" and "Ignore" buttons. """

    CANCEL_RETRY_CONTINUE = 6
    """ "Cancel", "Retry" and "Ignore" buttons. """

    RETRY_CANCEL = 7
    """ "Retry" and "Cancel" buttons. """

class MessageBoxResult(Enum):
    """ The message box resuld, based on user selection. """

    NONE = 0
    """ The user has cancelled the message box. """

    OK = 1
    """ The user has pressed the "OK" button. """

    CANCEL = 2
    """ The user has pressed the "Cancel" button. """

    YES = 3
    """ The user has pressed the "Yes" button. """

    NO = 4
    """ The user has pressed the "No" button. """

    ABORT = 5
    """ The user has pressed the "Abort" button. """

    RETRY = 6
    """ The user has pressed the "Retry" button. """

    IGNORE = 7
    """ The user has pressed the "Ignore" button. """

    CONTINUE = 8
    """ The user has pressed the "Continue" button. """

class MessageBox(Dialog):
    """ A modal dialog that shows a message (perhaps multiline)
        to the user and asks the user to make a choice (or close
        the dialog). """

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
                self.__pic1 = Label(self.__pan1,
                                    image = AwtResources.image("MessageBox.InformationIcon"))
            case MessageBoxIcon.QUESTION:
                self.__pic1 = Label(self.__pan1,
                                    image = AwtResources.image("MessageBox.QuestionIcon"))
            case MessageBoxIcon.ERROR:
                self.__pic1 = Label(self.__pan1,
                                    image = AwtResources.image("MessageBox.ErrorIcon"))
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
    #   Properties
    @property
    def result(self) -> MessageBoxResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Operations
    @staticmethod
    def show(parent: tk.BaseWidget,
             title: str,
             message: str,
             icon: MessageBoxIcon = MessageBoxIcon.NONE,
             buttons: MessageBoxButtons = MessageBoxButtons.OK):
        """ 
            Displays a modal message box.

            @param parent:
                The parent window for the message box.
            @param title:
                The title for the message box; must not be None.
            @param message:
                The message to display in the message box; must not be None.
            @param icon:
                The icon for the message box; must not be None.
            @param buttons:
                The message box buttons to display; must not be None.
        """
        with MessageBox(parent, title, message, icon, buttons) as mb:
            mb.do_modal()

    ##########
    #   Event listeners
    def __on_ok(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        self.__result = MessageBoxResult.OK
        self.end_modal()

    def __on_cancel(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        self.__result = MessageBoxResult.CANCEL
        self.end_modal()
