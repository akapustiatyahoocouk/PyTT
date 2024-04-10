#   Python standard library
from abc import ABC, abstractmethod, abstractproperty

#   Internal dependencies on modules within the same component
from .DatabaseAddress import DatabaseAddress
from .DatabaseType import DatabaseType

##########
#   Public entities
class Database(ABC):

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
