"""
    The message box modal dialog.
"""
#   Python standard library
from tkinter.messagebox import CANCEL
from typing import Any
from enum import Enum

#   Internal dependencies on modules within the same component
from .Dialog import Dialog

##########
#   Public entities
class MesageBoxIcon(Enum)
    NONE = 0    
    INFORMATION = 1
    QUESTION = 2
    ERROR = 3
    
class MessageBoxButtons(Enum)
    OK = 1
    OK_CANCEL = 2
    YES_NO = 3
    YES_NO_CANCEL = 4
    ABORT_RETRY_IGNORE = 5
    CANCEL_RETRY_CONTINUE = 6
    RETRY_CANCEL = 7

class MessageBoxResult(Enum)
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
    def __init__(self, title: str, message: Any, 
                 icon: MesageBoxIcon = MesageBoxIcon.NONE,
                 buttons: MessageBoxButtons = MessageBoxButtons.OK)
        assert isinstance(title, str)
        assert message is not None
        assert isinstance(icon, MesageBoxIcon)
        assert isinstance(buttons, MessageBoxButtons)

        #   Create controls