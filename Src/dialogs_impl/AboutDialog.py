"""
    Implements "About PyTT" modal dialog.
"""
from typing import final
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

import awt
import resources

@final
class AboutDialogResult(Enum):
    """ The result of modal invocation of the AboutDialog. """
    OK = 1
    """ Dialog closed, by whatever means necessary. """

@final
class AboutDialog(awt.Dialog):
    """ The modal "about..." dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: ttk.Widget):
        super().__init__(parent, 'About PyTT')
        self.__result = AboutDialogResult.OK

        #   Create controls
        self.__pan0 = ttk.Label(self)
        self.__pan1 = ttk.Label(self.__pan0)
        self.__pan2 = ttk.Label(self.__pan0)
        
        self.__pic1 = ttk.Label(self.__pan1, image = resources.Resources.PRODUCT_ICON)
        self.__msg1 = ttk.Label(self.__pan2, text = resources.Resources.PRODUCT_NAME, anchor=tk.CENTER)
        self.__msg2 = ttk.Label(self.__pan2, text = "Version " + resources.Resources.PRODUCT_VERSION, anchor=tk.CENTER)
        self.__msg3 = ttk.Label(self.__pan2, text = resources.Resources.PRODUCT_COPYRIGHT, anchor=tk.CENTER)
        self.__separator = ttk.Separator(self, orient="horizontal")
        self.__okButton = ttk.Button(self, text="OK", default="active", command=self.__on_ok)

        #   Set up control structure
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)
        self.__pan1.pack(side=tk.LEFT, padx=0, pady=0)
        self.__pan2.pack(fill=tk.X, padx=0, pady=0)

        self.__pic1.pack(fill=tk.NONE, padx=2, pady=2)
        self.__msg1.pack(fill=tk.X, padx=2, pady=2)
        self.__msg2.pack(fill=tk.X, padx=2, pady=2)
        self.__msg3.pack(fill=tk.X, padx=2, pady=2)
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__okButton.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.bind("<Escape>", self.__on_ok)
        self.bind("<Return>", self.__on_ok)
        self.protocol("WM_DELETE_WINDOW", self.__on_ok)

        #  Done
        self.__okButton.focus_set()

    ##########
    #   Properties    
    @property
    def result(self) -> AboutDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __on_ok(self, evt = None) -> None:
        self.destroy()
