#   Python standard library
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .DatabaseType import DatabaseType

##########
#   Public entities
class DatabaseAddress(ABC):
    """ A "database address" uniquely identifies the location of
        a database and is database type - specific."""

    ##########
    #   object
    def __str__(self) -> str:
        return self.display_form

    ##########
    #   Properties
    @abstractproperty
    def database_type(self) -> DatabaseType:
        """ The database type to which this database address belongs. """
        raise NotImplementedError()

    @abstractproperty
    def display_form(self) -> str:
        """ The user-readable display form of this database address. """
        raise NotImplementedError()

    @abstractproperty
    def external_form(self) -> str:
        """ The external (re-parsable) form of this database address. """
        raise NotImplementedError()

