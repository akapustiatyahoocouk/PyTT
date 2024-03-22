"""
    Implements "Login to PyTT" modal dialog.
"""
from typing import final, Optional, Callable
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

import awt
import ws

@final
class LoginDialogResult(Enum):
    """ The result of modal invocation of the LoginDialog. """
    OK = 1
    """ User has supplied the login details. """
    
    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class LoginDialog(awt.Dialog):
    """ The modal "login" dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: Optional[ttk.Widget], login: Optional[str] = None,
                 on_ok_callback: Callable[["LoginDialog"],None] = None, 
                 on_cancel_callback: Callable[["LoginDialog"],None] = None):
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
            @param on_ok_callback:
                The callback to invoke just before the login dialog is 
                closed successfully with login credentials specified, 
                None == no callback.
            @param on_cancel_callback:
                The callback to invoke just before the login dialog is 
                cancelled by the user, None == no callback.
        """
        super().__init__(parent, 'Login to PyTT')
        self.__on_ok_callback = on_ok_callback
        self.__on_cancel_callback = on_cancel_callback

        self.__result = LoginDialogResult.CANCEL
        self.__credentials = None
        
        #   Create control models
        self.__loginVar = tk.StringVar(value=login)
        self.__passwordVar = tk.StringVar()
        
        #   Create controls
        self.__pan0 = ttk.Label(self)
        
        self.__loginLabel = ttk.Label(self.__pan0, text = 'Login:', anchor=tk.E)
        self.__loginEntry = ttk.Entry(self.__pan0, width=40, textvariable=self.__loginVar)

        self.__passwordLabel = ttk.Label(self.__pan0, text = 'Password:', anchor=tk.E)
        self.__passwordEntry = ttk.Entry(self.__pan0, width=40, show="\u2022", textvariable=self.__passwordVar)
        
        self.__separator = ttk.Separator(self, orient="horizontal")

        self.__okButton = ttk.Button(self, text='OK', default="active")
        self.__cancelButton = ttk.Button(self, text='Cancel')

        #   Set up control structure
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)

        self.__loginLabel.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__loginEntry.grid(row=0, column=1, padx=2, pady=2, sticky="W")

        self.__passwordLabel.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__passwordEntry.grid(row=1, column=1, padx=2, pady=2, sticky="W")
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancelButton.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__okButton.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.__loginVar.trace_add("write", self.__refresh)
        self.__passwordVar.trace_add("write", self.__refresh)
        
        self.bind("<Escape>", self.__on_cancel)
        self.bind("<Return>", self.__on_ok)
        self.protocol("WM_DELETE_WINDOW", self.__on_cancel)
        self.__okButton.bind("<Button-1>", self.__on_ok)
        self.__cancelButton.bind("<Button-1>", self.__on_cancel)
        
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
    def credentials(self) -> Optional[ws.Credentials]:
        """ The entered user credentials or None if the dialog
            was cancelled by the user. """
        return self.__credentials
    
    ##########
    #   Implementation helpers
    def __refresh(self, *args) -> None:
        login : str = self.__loginVar.get()
        if len(login.strip()) == 0:
            self.__passwordLabel.state(["disabled"])
            self.__passwordEntry.state(["disabled"])
            self.__okButton.state(["disabled"])
        else:
            self.__passwordLabel.state(["!disabled"])
            self.__passwordEntry.state(["!disabled"])
            self.__okButton.state(["!disabled"])
    
    ##########
    #   Event listeners    
    def __on_ok(self, evt = None) -> None:
        login = self.__loginVar.get()
        password = self.__passwordVar.get()
        self.__credentials = ws.Credentials(login, password)
        self.__result = LoginDialogResult.OK
        if self.__on_ok_callback is not None:
            self.__on_ok_callback(self) 
        self.destroy()

    def __on_cancel(self, evt = None) -> None:
        self.__credentials = None
        self.__result = LoginDialogResult.CANCEL
        if self.__on_cancel_callback is not None:
            self.__on_cancel_callback(self) 
        self.destroy()
