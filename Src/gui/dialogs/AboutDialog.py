"""
    Implements "About PyTT" modal dialog.
"""
#   Python standard library
from typing import final
from enum import Enum
import tkinter as tk

from awt.Dialog import Dialog
from awt.Label import Label
from awt.Separator import Separator
from awt.Button import Button
from util.api import *

@final
class AboutDialogResult(Enum):
    """ The result of modal invocation of the AboutDialog. """
    OK = 1
    """ Dialog closed, by whatever means necessary. """

@final
class AboutDialog(Dialog):
    """ The modal "about..." dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: tk.BaseWidget):
        Dialog.__init__(self, parent, 'About PyTT')
        self.__result = AboutDialogResult.OK

        #   Create controls
        self.__pan0 = Label(self)
        self.__pan1 = Label(self.__pan0)
        self.__pan2 = Label(self.__pan0)
        
        self.__pic1 = Label(self.__pan1, image = UtilResources.image("PyTT.LargeImage"))
        self.__msg1 = Label(self.__pan2, text = UtilResources.string("PyTT.ProductName"), anchor=tk.CENTER)
        self.__msg2 = Label(self.__pan2, text = "Version " + UtilResources.string("PyTT.ProductVersion"), anchor=tk.CENTER)
        self.__msg3 = Label(self.__pan2, text = UtilResources.string("PyTT.ProductCopyright"), anchor=tk.CENTER)
        self.__separator = Separator(self, orient="horizontal")
        self.__ok_button = Button(self, text="OK", command=self.__on_ok)

        #   Set up control structure
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)
        self.__pan1.pack(side=tk.LEFT, padx=0, pady=0)
        self.__pan2.pack(fill=tk.X, padx=0, pady=0)

        self.__pic1.pack(fill=tk.NONE, padx=2, pady=2)
        self.__msg1.pack(fill=tk.X, padx=2, pady=2)
        self.__msg2.pack(fill=tk.X, padx=2, pady=2)
        self.__msg3.pack(fill=tk.X, padx=2, pady=2)
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__ok_button

        self.__ok_button.add_action_listener(self.__on_ok)

        #  Done
        self.__ok_button.focus_set()

    ##########
    #   Properties    
    @property
    def result(self) -> AboutDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __on_ok(self, evt = None) -> None:
        self.end_modal()
