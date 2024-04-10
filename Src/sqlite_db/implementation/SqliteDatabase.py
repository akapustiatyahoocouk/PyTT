#   Python standard library
import sqlite3

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqliteDatabaseType import SqliteDatabaseType
from .SqliteDatabaseAddress import SqliteDatabaseAddress

##########
#   Public entities
@final
class SqliteDatabase(Database):

    ##########
    #   Construction
    def __init__(self, 
                 address: SqliteDatabaseAddress,
                 connection: sqlite3.Connection):
        assert isinstance(address, SqliteDatabaseAddress)
        assert isinstance(connection, sqlite3.Connection)

        self.__address = address
        self.__connection = connection
        self.__is_open = True

    ##########
    #   Database - Properties
    @property
    def type(self) -> DatabaseType:
        return SqliteDatabaseType.instance

    @property
    def address(self) -> DatabaseAddress:
        return self.__address

    @property
    def is_open(self) -> bool:
        return self.__is_open

    ##########
    #   Database - Operations (general)
    def close(self) -> None:
        if self.__is_open:
            try:
                self.__connection.close()
            except Exception as ex:
                raise DatabaseIoError(str(ex)) from ex
            finally:
                self.__is_open = False
