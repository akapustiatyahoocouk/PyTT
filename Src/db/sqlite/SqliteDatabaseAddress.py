#   Python standard library

#   Dependencies on other PyTT components
from db.DatabaseAddress import DatabaseAddress

class SqliteDatabaseAddress(DatabaseAddress):
    """ An address of a SQLite database is its full path. """

    ##########
    #   Construction
    def __init__(self, path: str):
        self.__path = os.path.abspath(path)

    ##########7
    #   DatabaseAddress - Properties
    @property
    def database_type(self) -> "SqliteDatabaseType":
        """ The database type to which this database address belongs. """
        return db.sqlite_impl.SqliteDatabaseType.SqliteDatabaseType.instance()

    @property
    def display_form(self) -> str:
        """ The user-readable display form of this database address. """
        return self.__path

    @property
    def external_form(self) -> str:
        """ The external (re-parsable) form of this database address. """
        return self.__path
