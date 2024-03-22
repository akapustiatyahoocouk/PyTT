from typing import final, Optional

import ws_impl.Credentials

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
    def get() -> Optional[ws_impl.Credentials.Credentials]:
        return CurrentCredentials.__currentCredentials

    @staticmethod
    def set(cc: ws_impl.Credentials.Credentials) -> None:
        assert cc is not None
        CurrentCredentials.__currentCredentials = cc


