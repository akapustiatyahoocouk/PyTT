"""
    Implements "Login to PyTT" modal dialog.
"""
#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

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
            Constructs the locin dialog.
        
            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used), 
                None == no parent.
            @param login:
                The login identifier to initially display in the "login"
                field or None. If spefified, the initial keyboard focus 
                goes straight to the "password" field.
        """
        super().__init__(parent, 'Login to PyTT')

        self.__result = LoginDialogResult.CANCEL
        self.__credentials = None
        
        #   Create control models
        self.__loginVar = tk.StringVar(value=login)
        self.__passwordVar = tk.StringVar()
        
        #   Create controls
        self.__pan0 = Label(self)
        
        self.__loginLabel = Label(self.__pan0, text = 'Login:', anchor=tk.E)
        self.__loginEntry = Entry(self.__pan0, width=40, textvariable=self.__loginVar)

        self.__passwordLabel = Label(self.__pan0, text = 'Password:', anchor=tk.E)
        self.__passwordEntry = Entry(self.__pan0, width=40, show="\u2022", textvariable=self.__passwordVar)
        
        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self, text='OK')
        self.__cancel_button = Button(self, text='Cancel')

        #   Set up control structure
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)

        self.__loginLabel.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__loginEntry.grid(row=0, column=1, padx=2, pady=2, sticky="W")

        self.__passwordLabel.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__passwordEntry.grid(row=1, column=1, padx=2, pady=2, sticky="W")
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__loginVar.trace_add("write", self.__refresh)
        self.__passwordVar.trace_add("write", self.__refresh)
        
        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Set initial focus & we're done
        if login is not None:
            self.__passwordEntry.focus_set()
        else:
            self.__loginEntry.focus_set()
        self.__refresh()
        
        self.wait_visibility()
        self.center_in_parent()

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
    #   Implementation helpers
    def __refresh(self, *args) -> None:
        login : str = self.__loginVar.get()
        if len(login.strip()) == 0:
            self.__passwordLabel.state([tk.DISABLED])
            self.__passwordEntry.state(["disabled"])
            self.__ok_button.enabled = False
        else:
            self.__passwordLabel.state(["!disabled"])
            self.__passwordEntry.state(["!disabled"])
            self.__ok_button.enabled = True
    
    ##########
    #   Event listeners    
    def __on_ok(self, evt = None) -> None:
        if "disabled" in self.__ok_button.state():
            return
        login = self.__loginVar.get()
        password = self.__passwordVar.get()
        self.__credentials = Credentials(login, password)
        self.__result = LoginDialogResult.OK
        self.end_modal()

    def __on_cancel(self, evt = None) -> None:
        self.__credentials = None
        self.__result = LoginDialogResult.CANCEL
        self.end_modal()
