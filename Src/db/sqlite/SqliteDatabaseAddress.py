import os

import db.api as dbapi
import db.sqlite.SqliteDatabaseType

class SqliteDatabaseAddress(dbapi.IDatabaseAddress):
    """ An address of a SQLite database is its full path. """

    ##########
    #   Construction
    def __init__(self, path: str):
        self.__path = os.path.abspath(path)

    ##########7
    #   IDatabaseAddress - Properties
    @property
    def database_type(self) -> 'SqliteDatabaseType':
        """ The database type to which this database address belongs. """
        return db.sqlite.SqliteDatabaseType.SqliteDatabaseType.instance()

    @property
    def display_form(self) -> str:
        """ The user-readable display form of this database address. """
        return self.__path

    @property
    def external_form(self) -> str:
        """ The external (re-parsable) form of this database address. """
        return self.__path
