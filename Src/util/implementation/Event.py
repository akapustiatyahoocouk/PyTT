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
        """
            Constructs the event with the specified source.

            @param source:
                The event source, cannot be None.
        """
        assert source is not None
        self.__source = source
        self.__processed = False

    ##########
    #   Properties
    @property
    def source(self) -> Any:
        """ The source that has raised this event; never None. """
        return self.__source

    @property
    def processed(self) -> bool:
        """ True if this event has already been processed and requires
            no further processing, else False. """
        return self.__processed

    @processed.setter
    def processed(self, new_processed: bool) -> None:
        """ Set to True if this event has been processed and
            requires no further processing, else to False. """
        assert isinstance(new_processed, bool)
        self.__processed = new_processed
