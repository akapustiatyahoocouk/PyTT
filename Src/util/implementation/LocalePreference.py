#   Python standard library
from typing import Optional

#   Internal dependencies on modules within the same component
from .Preference import Preference
from .Locale import Locale

##########
#   Public entities
class LocalePreference(Preference):
    """ A "preference" whose value is Locale or None. """

    ##########
    #   Construction (from derived classes only)
    def __init__(self, name: str, default_value: Optional[Locale]) -> None:
        Preference.__init__(self, name, default_value)
        assert (default_value is None) or isinstance(default_value, Locale)
        
        self.__value = default_value

    ##########
    #   Preference - Properties
    @property
    def default_value(self) -> Optional[Locale]:
        return Preference.default_value(self)

    @property
    def value(self) -> Optional[Locale]:
        return self.__value

    @value.setter
    def value(self, new_value: Optional[Locale]) -> None:
        assert (new_value is None) or isinstance(new_value, Locale)
        self.__value = new_value
