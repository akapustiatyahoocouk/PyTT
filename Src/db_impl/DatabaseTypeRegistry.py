from typing import final, Optional

from util import staticproperty
from db_impl.IDatabaseType import IDatabaseType

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

    @staticproperty
    def all_database_types() -> set[IDatabaseType]:
        """ The 'set' of all registered database types. """
        return set(DatabaseTypeRegistry.__registry.values())

