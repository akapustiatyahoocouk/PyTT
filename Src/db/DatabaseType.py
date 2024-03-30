from typing import Optional
from abc import ABC, abstractproperty, abstractmethod

from util.Annotations import staticproperty

class DatabaseType(ABC):
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
    def parse_database_address(self, externa_form: str) -> "DatabaseAddress":
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
    def default_database_address(self) -> "DatabaseAddress":
        raise NotImplementedError()

    ##########
    #   Registry
    __registry : dict[str, "DatabaseType"] = {}

    @staticmethod
    def register(database_type: "DatabaseType") -> bool:
        """ "Registers" the specified database type.
            Returns True on  success, False on failure. """
        assert isinstance(database_type, DatabaseType)
        
        print('Registering', database_type.display_name, 'database type [' + 
              database_type.mnemonic + ']')
        if database_type.mnemonic in DatabaseType.__registry:
            return DatabaseType.__registry[database_type.mnemonic] is database_type
        else:
            DatabaseType.__registry[database_type.mnemonic] = database_type
            return True
        
    @staticmethod
    def find(mnemonic: str) -> Optional["DatabaseType"]:
        """ Finds a registered database type by mnemonic;
            returns None if not found. """
        return DatabaseType.__registry.get(mnemonic, None)

    @staticproperty
    def all() -> set["DatabaseType"]:
        """ The 'set' of all registered database types. """
        return set(DatabaseType.__registry.values())
