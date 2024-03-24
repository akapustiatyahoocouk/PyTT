#   Python standard library
from typing import Optional

#   Internal dependencies on modules within the same component
from util.implementation.Preference import Preference

##########
#   Public entities
class BoolPreference(Preference):
    """ A "preference" whose value is bool or None. """

    ##########
    #   Construction (from derived classes only)
    def __init__(self, name: str, default_value: Optional[bool]) -> None:
        Preference.__init__(self, name, default_value)
        assert (default_value is None) or isinstance(default_value, bool)
        
        self.__value = default_value

    ##########
    #   Preference - Properties
    @property
    def default_value(self) -> Optional[bool]:
        return Preference.default_value(self)

    @property
    def value(self) -> Optional[bool]:
        return self.__value

    @value.setter
    def value(self, new_value: Optional[bool]) -> None:
        assert (new_value is None) or isinstance(new_value, bool)
        self.__value = new_value
