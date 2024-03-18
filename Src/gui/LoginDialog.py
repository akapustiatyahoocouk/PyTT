"""
    Implements "Login to PyTT" modal dialog.
"""

from typing import final, Optional

import tkinter as tk
import tkinter.ttk as ttk

from gui.Dialog import *

@final
class LoginDialogResult(Enum):
    """ The result of modal invocation of the LoginDialog. """
    OK = 1      #   User has supplied the login details
    CANCEL = 2  #   Dialog cancelled by user

@final
class LoginDialog(Dialog):
    """ The modal 'login' dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: Optional[ttk.Widget], login: Optional[str] = None):
        super().__init__(parent, 'Login to PyTT')
        self.__result = LoginDialogResult.CANCEL
        
        #   Create control models
        self.__loginVar = tk.StringVar(value=login)
        self.__passwordVar = tk.StringVar()
        
        #   Create controls
        self.__pan0 = ttk.Label(self.root)
        
        self.__loginLabel = ttk.Label(self.__pan0, text = 'Login:', anchor=tk.E)
        self.__loginEntry = ttk.Entry(self.__pan0, width=20, textvariable=self.__loginVar)

        self.__passwordLabel = ttk.Label(self.__pan0, text = 'Password:', anchor=tk.E)
        self.__passwordEntry = ttk.Entry(self.__pan0, width=20, show='\u2022', textvariable=self.__passwordVar)
        
        self.__separator = ttk.Separator(self.root, orient='horizontal')

        self.__okButton = ttk.Button(self.root, text="OK", default='active')
        self.__cancelButton = ttk.Button(self.root, text="Cancel")

        #   Set up control structure
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)

        self.__loginLabel.grid(row=0, column=0, padx=2, pady=2, sticky='W')
        self.__loginEntry.grid(row=0, column=1, padx=2, pady=2, sticky='W')

        self.__passwordLabel.grid(row=1, column=0, padx=2, pady=2, sticky='W')
        self.__passwordEntry.grid(row=1, column=1, padx=2, pady=2, sticky='W')
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancelButton.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__okButton.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.__loginVar.trace_add("write", self.__refresh)
        self.__passwordVar.trace_add("write", self.__refresh)
        
        self.root.bind('<Escape>', self.__onCancel)
        self.root.bind('<Return>', self.__onOk)
        self.root.protocol("WM_DELETE_WINDOW", self.__onCancel)
        self.__okButton.bind("<Button-1>", self.__onCancel)
        self.__cancelButton.bind("<Button-1>", self.__onCancel)
        
        #   Set initial focus & we're done
        if login is not None:
            self.__passwordEntry.focus_set()
        else:
            self.__loginEntry.focus_set()
        self.__refresh()

    ##########
    #   Properties    
    @property
    def result(self) -> LoginDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __refresh(self, *args):
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
    def __onOk(self, evt = None):
        login = self.__loginVar.get()
        password = self.__passwordVar.get()
        self.__result = LoginDialogResult.OK
        self.root.destroy()
        pass

    def __onCancel(self, evt = None):
        self.__result = LoginDialogResult.CANCEL
        login = self.__loginVar.get()
        password = self.__passwordVar.get()
        self.root.destroy()
        pass
