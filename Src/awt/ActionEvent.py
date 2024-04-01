"""
    Defines the ActionEvent API.
"""
#   Python standard library
from typing import TypeAlias, Callable

#   Internal dependencies on modules within the same component
from awt.Event import Event

class ActionEvent(Event):
    """ An "action" event - signals that an action has occurred
        in the event source (e.g. a Button is pressed, etc.) """

    ##########
    #   Construction
    def __init__(self, source):
        """ Constructs the event. """
        Event.__init__(self, source)

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
