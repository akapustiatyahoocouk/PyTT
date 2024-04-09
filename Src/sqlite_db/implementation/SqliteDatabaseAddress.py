#   Python standard library

#   Dependencies on other PyTT components
from db.interface.api import *

##########
#   Public entities
class SqliteDatabaseAddress(DatabaseAddress):
    """ An address of a SQLite database is its full path. """

    ##########
    #   Construction
    def __init__(self, path: str):
        self.__path = os.path.abspath(path)

    ##########
    #   object
    def __hash__(self) -> int:
        return hash(self.__path)
    
    def __str__(self) -> str:
        return self.__path

    def __repr__(self) -> str:
        return self.__path

    def __eq__(self, op2) -> bool:
        if isinstance(op2, SqliteDatabaseAddress):
            return self.__path == op2.__path
        return False

    def __ne__(self, op2) -> bool:
        if isinstance(op2, SqliteDatabaseAddress):
            return self.__path != op2.__path
        return True

    ##########
    #   DatabaseAddress - Properties
    @property
    def database_type(self) -> "SqliteDatabaseType":
        """ The database type to which this database address belongs. """
        return sqlite_db.implementation.SqliteDatabaseType.SqliteDatabaseType.instance()

    @property
    def display_form(self) -> str:
        """ The user-readable display form of this database address. """
        return self.__path

    @property
    def external_form(self) -> str:
        """ The external (re-parsable) form of this database address. """
        return self.__path
