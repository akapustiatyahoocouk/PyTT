"""
    The error report modal dialog.
"""
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
from enum import Enum

from .ActionEvent import ActionEvent

#   Internal dependencies on modules within the same component
from .Dialog import Dialog
from .Panel import Panel
from .Label import Label
from .Separator import Separator
from .Button import Button
from .MessageBox import MessageBox, MessageBoxIcon, MessageBoxButtons
from awt.resources.AwtResources import AwtResources

##########
#   Public entities
class ErrorDialog(Dialog):

    ##########
    #   Operations
    @staticmethod
    def show(parent: tk.BaseWidget, error: [str|Exception]):
        if isinstance(error, str):
            MessageBox.show(parent,
                            'Error',
                            error,
                            icon=MessageBoxIcon.ERROR,
                            buttons=MessageBoxButtons.OK)
        else:
            assert isinstance(error, Exception)
            raise NotImplementedError()

    ##########
    #   Event listeners
    def __on_ok(self, evt: ActionEvent) -> None:
        self.end_modal()
