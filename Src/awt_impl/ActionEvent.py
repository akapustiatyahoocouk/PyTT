from typing import final, Optional, TypeAlias, Callable
from enum import Enum

from awt_impl.Event import Event

class ActionEvent(Event):
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


ActionListener: TypeAlias = Callable[[ActionEvent], None]
""" A signature of a listener to action events - a function
    or a bound method. """
