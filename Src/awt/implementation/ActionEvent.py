""" Defines the ActionEvent API. """

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
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
