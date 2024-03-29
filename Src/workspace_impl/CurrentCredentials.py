from typing import final, Optional

from workspace_impl.Credentials import Credentials

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

    #   TODO Move this class' logic into the static "Credentials.current" property ?        
    @staticmethod
    def get() -> Optional[Credentials]:
        return CurrentCredentials.__currentCredentials

    @staticmethod
    def set(cc: Credentials) -> None:
        assert isinstance(cc, Credentials)

        if cc is not CurrentCredentials.__currentCredentials:
            CurrentCredentials.__currentCredentials = cc
            #   TODO do we need to notify listeners of the "current" workspace change ?


