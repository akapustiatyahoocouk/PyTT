#   Python standard library
from typing import final, Optional

#   Internal dependencies on modules within the same component
from workspace.implementation.Credentials import Credentials

##########
#   Public entities
#   TODO Move this class' logic into the static "Credentials.current" property ?        
@final
class CurrentCredentials:
    """ The "current" credentials. """

    ##########
    #   Implementation
    __currentCredentials = None
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

    @staticmethod
    def get() -> Optional[Credentials]:
        return CurrentCredentials.__currentCredentials

    @staticmethod
    def set(cc: Credentials) -> None:
        assert isinstance(cc, Credentials)

        if cc is not CurrentCredentials.__currentCredentials:
            CurrentCredentials.__currentCredentials = cc
            #   TODO do we need to notify listeners of the "current" workspace change ?


