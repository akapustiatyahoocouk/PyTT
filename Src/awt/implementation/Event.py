#   Python standard library
from abc import ABC
from typing import Any

##########
#   Public entities
class Event(ABC):
    """ The common base class for all events. """

    ##########
    #   Construction
    def __init__(self, source):
        """ Constructs the event with the specified source. """
        self.__source = source

    ##########
    #   Properties
    @property
    def source(self) -> Any:
        """ The source that has raised this event. """
        return self.__source

