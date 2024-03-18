"""
    Implements "About PyTT" modal dialog.
"""

import abc
from enum import Enum

from typing import final

import tkinter as tk
import tkinter.ttk as ttk

from gui.Dialog import *
from util.resources import *

@final
class AboutDialogResult(Enum):
    """ The result of modal invocation of the AboutDialog. """
    OK = 1      #   Dialog closed, by whatever means necessary

@final
class AboutDialog(Dialog):
    """ The modal 'about...' dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: ttk.Widget):
        super().__init__(parent, 'About PyTT')

        self.__result = AboutDialogResult.OK
        
        self.__pan0 = ttk.Label(self.root)
        self.__pan1 = ttk.Label(self.__pan0)
        self.__pan2 = ttk.Label(self.__pan0)
        
        self.__pic1 = ttk.Label(self.__pan1, image = UtilResources.PRODUCT_ICON)
        self.__msg1 = ttk.Label(self.__pan2, text = UtilResources.PRODUCT_NAME, anchor=tk.CENTER)
        self.__msg2 = ttk.Label(self.__pan2, text = "Version " + UtilResources.PRODUCT_VERSION, anchor=tk.CENTER)
        self.__msg3 = ttk.Label(self.__pan2, text = UtilResources.PRODUCT_COPYRIGHT, anchor=tk.CENTER)
        self.__separator = ttk.Separator(self.root, orient='horizontal')
        self.__closeButton = ttk.Button(self.root, text="Close", default='active')

        self.__pan0.pack(fill=tk.X, padx=0, pady=0)
        self.__pan1.pack(side=tk.LEFT, padx=0, pady=0)
        self.__pan2.pack(fill=tk.X, padx=0, pady=0)

        self.__pic1.pack(fill=tk.NONE, padx=2, pady=2)
        self.__msg1.pack(fill=tk.X, padx=2, pady=2)
        self.__msg2.pack(fill=tk.X, padx=2, pady=2)
        self.__msg3.pack(fill=tk.X, padx=2, pady=2)
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__closeButton.pack(side=tk.RIGHT, padx=0, pady=0)

        self.root.bind('<Escape>', self.__close)
        self.root.bind('<Return>', self.__close)
        self.__closeButton.bind("<Button-1>", self.__close)
        self.root.protocol("WM_DELETE_WINDOW", self.__close)

        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
        #self.root.wait_visibility()         # <<< NOTE
        #self.root.grab_set()                # <<< NOTE
        #self.root.transient(self.parent)    # <<< NOTE

        #self.__root.tkraise()
        #self.__root.update_idletasks()
        #self.__root.focus_force()
        self.__closeButton.focus_set()

    ##########
    #   Properties    
    @property
    def result(self) -> AboutDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __close(self, evt = None):
        #self.root.grab_release()      # <<< NOTE
        self.root.destroy()
        pass
