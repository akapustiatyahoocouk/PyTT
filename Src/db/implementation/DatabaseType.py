#   Python standard library
from typing import Optional
from abc import ABC, abstractproperty, abstractmethod
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
class DatabaseType(ABCWithConstants):
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
    def parse_database_address(self, external_form: str) -> "DatabaseAddress":
        """
            Parses an external (re-parsable) form of a database address
            of this type.
            
            @param external_form:
                The external (re-parsable) form of a database address.
            @return:
                The parsed database address.
            @raise InvalidDatabaseAddressException:
                If the specified external form of a database address
                does not make sense for this database type.
        """
        raise NotImplementedError()

    @abstractproperty
    def default_database_address(self) -> "DatabaseAddress":
        """ The address of the "default" database of this type;
            None if this database type has no concept of and
            "default" database. """
        raise NotImplementedError()

    @abstractmethod
    def enter_new_database_address(self, parent: tk.BaseWidget) -> "DatabaseAddress":
        """
            Prompts the user to interactively specify an address
            for a new database of this type.
    
            @param parent:
                The widget to use as a "parent" widget for any modal
                dialog(s) used during database address entry; None
                to use the GuiRoot.
            @return:
                The database address specified by the user; None 
                if the user has cancelled the process of database
                address entry.
        """
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
