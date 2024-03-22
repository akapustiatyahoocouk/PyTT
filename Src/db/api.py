"""
    Defines a low-level (data storage) database API.
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import final, Optional, TypeAlias
import uuid

Oid: TypeAlias = uuid.UUID

class IDatabaseType(ABC):
    """ A "database type" corresponds to a technology used to
        keep the data persistent (database engine type, etc.)"""
    
    ##########
    #   object
    def __str__(self) -> str:
        return self.display_name

    ##########
    #   Properties (general)
    @abstractproperty
    def mnemonic(self) -> str:
        """ The mnemonic identifier of this database type. """
        raise NotImplementedError()

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this database type. """
        raise NotImplementedError()

    ##########
    #   Database address handling
    @abstractmethod
    def parse_database_address(self, externa_form: str) -> "IDatabaseAddress":
        """
            Parses an external (re-parsable) form of a database address
            of this type.
            
            @param externa_form:
                The external (re-parsable) form of a database address.
            @return:
                The parsed database address.
            @raise InvalidDatabaseAddressException:
                If the specified external form of a database address
                doesnot make sense for this database type.
        """
        raise NotImplementedError()

    @abstractproperty
    def default_database_address(self) -> "IDatabaseAddress":
        raise NotImplementedError()


@final
class DatabaseTypeRegistry:
    """ The registry of known database types. 
        This is an utility class, never to be instantiated."""

    ##########
    #   Implementation data
    __registry : dict[str, IDatabaseType] = {}

    ##########
    #   Construction - not allowed - this is an utility class
    def __init__(self):
        raise NotImplementedError()

    ##########
    #   Operations
    @staticmethod
    def register_database_type(dbtype: IDatabaseType) -> bool:
        """ "Registers" the specified database type.
            Returns True on  success, False on failure. """
        print('Registering', dbtype.display_name, 'database type [' + dbtype.mnemonic + ']')
        if dbtype.mnemonic in DatabaseTypeRegistry.__registry:
            return DatabaseTypeRegistry.__registry[dbtype.mnemonic] is dbtype
        else:
            DatabaseTypeRegistry.__registry[dbtype.mnemonic] = dbtype
            return True
        
    @staticmethod
    def find_database_type(mnemonic: str) -> Optional[IDatabaseType]:
        """ Finds a registered database type by mnemonic;
            returns None if not found. """
        return DatabaseTypeRegistry.__registry.get(mnemonic, None)

    @staticmethod
    def get_all_database_types() -> set[IDatabaseType]:
        """ Returns a 'set' of all registered database types. """
        return set(DatabaseTypeRegistry.__registry.values())


class IDatabaseAddress(ABC):
    """ A "database address" uniquely identifies the location of
        a database and is database type - specific."""
    
    ##########
    #   object
    def __str__(self) -> str:
        return self.display_form
    
    ##########
    #   Properties
    @abstractproperty
    def database_type(self) -> IDatabaseType:
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
