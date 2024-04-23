#   Python standard library
from abc import ABC, abstractproperty
from typing import Any

##########
#   Public entities
class Preference(ABC):
    """ A "preference" is a single persistent data item
        that can be grouped into a given Preferences. """

    ##########
    #   Construction (from derived classes only)
    def __init__(self, name: str, default_value: Any) -> None:
        assert isinstance(name, str) and name.isidentifier()

        self.__name = name
        self.__default_value = default_value

    ##########
    #   Properties
    @property
    def name(self) -> str:
        """ The internal name of this preference, """
        return self.__name

    @property
    def default_value(self) -> Any:
        """ The default value of this preference, """
        return self.__default_value

    @abstractproperty
    def value(self) -> Any:
        """ The current value of this preference. """
        raise NotImplementedError()

    @value.setter
    def value(self, new_value: Any) -> None:
        """ Sets the current value of this preference. """
        raise NotImplementedError()
