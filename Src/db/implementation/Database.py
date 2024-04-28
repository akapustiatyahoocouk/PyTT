""" A persistent container where data is kept. """

#   Python standard library
from typing import List
from abc import ABC, abstractmethod, abstractproperty

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseAddress import DatabaseAddress
from .DatabaseType import DatabaseType
from .Exceptions import AccessDeniedError

##########
#   Public entities
class Database(ABC):
    """ A persistent container where data is kept. """
    
    ##########
    #   object (entry/exit protocol needed for Dialog.do_modal
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        try:
            self.close()
        except:
            pass    #   TODO log

    ##########
    #   Properties
    @abstractproperty
    def type(self) -> DatabaseType:
        """ The type of this database; can be safely obtained
            for both open and closed databases. """
        raise NotImplementedError()

    @abstractproperty
    def address(self) -> DatabaseAddress:
        """ The address of this database; can be safely obtained
            for both open and closed databases. """
        raise NotImplementedError()

    @abstractproperty
    def is_open(self) -> bool:
        """ True if this Database is currently open (i.e. can be
            used to access the physical database), False if closed. """
        raise NotImplementedError()

    ##########
    #   Operations (general)
    @abstractmethod
    def close(self) -> None:
        """
            Closes this Database; has no effect if already closed.

            @raise DatabaseError:
                If an error occurs; the Database object is
                still "closed" before the exception is thrown.
        """
        raise NotImplementedError()

    ##########
    #   Operations (associations)
    @abstractmethod
    def try_login(self, login: str, password: str) -> Optional["Account"]:
        """
            Attempts a login. If the account with the specified
            login and password exists in this database, is enabled
            and belongs to an enabled user, then returns it; else
            returns None.

            @param login:
                The account login.
            @param password:
                The account password.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    def login(self, login: str, password: str) -> Optional["Account"]:
        """
            Performs a login. If the account with the specified
            login and password exists in this database, is enabled
            and belongs to an enabled user, then returns it; else
            an error occurs.

            @param login:
                The account login.
            @param password:
                The account password.
            @raise DatabaseError:
                If an error occurs.
        """
        assert isinstance(login, str)
        assert isinstance(password, str)

        account = self.try_login(login, password)
        if account is None:
            raise AccessDeniedError()
        return account

    ##########
    #   Operations (life cycle)
    @abstractmethod
    def create_user(self,
                    enabled: bool = True,
                    real_name: str = None,  #   MUST specify!
                    inactivity_timeout: Optional[int] = None,
                    ui_locale: Optional[Locale] = None,
                    email_addresses: List[str] = []) -> "User":
        """
            Creates a new User.

            @param enabled:
                True to create an initially enabled User, False
                to create an initially disabled User.
            @param real_name:
                The "real name" for the new User.
            @param inactivity_timeout:
                The inactivity timeout for the new User, expressed
                in minutes, or None if the new user shall have no
                inactivity timeout.
            @param ui_locale:
                The preferred UI locale for the new User, or None if
                the new user shall have no preferred UI locale (and will
                be therefore using the system/default UI Locale).
            @param email_addresses:
                The list of e-mail addresses for the new User;
                cannot be None or contain Nones, but can be empty.
            @return:
                The newly created User.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
