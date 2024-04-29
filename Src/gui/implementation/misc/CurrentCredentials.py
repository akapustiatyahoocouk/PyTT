""" The "current" credentials. Placed in the gui component
    and not in the workspace component because the notion
    of the "current" Credentials is entirely a gui phenomenon. """

#   Python standard library
from typing import final, Optional

#   Dependencies on other PyTT components
from workspace.interface.api import *

##########
#   Public entities
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

    ##########
    #   Operations    
    @staticmethod
    def get() -> Optional[Credentials]:
        """ The "current" Credentials, None if there isn't any. """
        return CurrentCredentials.__current_credentials

    @staticmethod
    def set(cc: Credentials) -> None:
        """ Sets the "current" Credentials, cannot be set to None. """
        assert isinstance(cc, Credentials)

        if cc is not CurrentCredentials.__current_credentials:
            CurrentCredentials.__current_credentials = cc
            #   TODO notify listeners of the "current" credentials change
