from typing import final, Optional
from enum import Enum
import tkinter as tk

import awt_impl.Event

class ActionEvent(awt_impl.Event.Event):
    """ An "action" event - signals that an action has occurred
        in the event source (e.g. a Button is pressed, etc.) """

    ##########
    #   Construction
    def __init__(self, source):
        """ Constructs the event. """
        super().__init__(source)

    ##########
    #   object
    def __str__(self) -> str:
        result = ""
        if self.source is not None:
            result += "source="
            result += str(self.source)
        return "ActionEvent(" + result + ")"
