#   Python standard library
from typing import final, Optional

#   Internal dependencies on modules within the same component
from .Credentials import Credentials

##########
#   Public entities
#   TODO Move this class' logic into the static "Credentials.current" property ?
@final
class CurrentCredentials:
    """ The "current" credentials. """

    ##########
    #   Implementation
    __current_credentials = None

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

    @staticmethod
    def get() -> Optional[Credentials]:
        return CurrentCredentials.__current_credentials

    @staticmethod
    def set(cc: Credentials) -> None:
        assert isinstance(cc, Credentials)

        if cc is not CurrentCredentials.__current_credentials:
            CurrentCredentials.__current_credentials = cc
            #   TODO notify listeners of the "current" credentials change
