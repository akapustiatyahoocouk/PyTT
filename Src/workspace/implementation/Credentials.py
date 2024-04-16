#   Python standard library
from typing import final, Optional
import hashlib

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class Credentials:
    """ The user's credentials. """
    
    ##########
    #   Construction
    def __init__(self, login: str, password: str):
        """
            Constructs the user's credentials.
            
            @param login:
                The user's login identifier; must be a string.
            @param password:
                The user's password; must be a string.
        """
        assert isinstance(login, str)
        assert isinstance(password, str)
        
        self.__login = login;
        self.__password = password
        self.__password_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        
    ##########
    #   object    
    def __hash__(self) -> int:
        return hash(self.__login())
    
    #   a Credentials instance compares "less than" any other instance
    def __eq__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return False
        return ((self.__login == other.__login) and
                (self.__password_hash == other.__password_hash))

    def __ne__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return True
        return ((self.__login != other.__login) or
                (self.__password_hash != other.__password_hash))

    def __lt__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return True
        return ((self.__login < other.__login) or
                ((self.__login == other.__login) and    
                 (self.__password_hash < other.__password_hash)))

    def __le__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return True
        return ((self.__login < other.__login) or
                ((self.__login == other.__login) and    
                 (self.__password_hash <= other.__password_hash)))

    def __gt__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return False
        return ((self.__login > other.__login) or
                ((self.__login == other.__login) and    
                 (self.__password_hash > other.__password_hash)))

    def __ge__(self, other) -> bool:
        assert isinstance(self, Credentials)
        if not isinstance(other, Credentials):
            return False
        return ((self.__login > other.__login) or
                ((self.__login == other.__login) and    
                 (self.__password_hash >= other.__password_hash)))

    ##########
    #   Properties
    @property
    def login(self) -> str:
        """ The user's login identifier. """
        return self.__login
    
    @property
    def password_hash(self) -> str:
        """ The uppercase hex string representing the SHA-1 hash 
            of the user's password. """
        return self.__password_hash
