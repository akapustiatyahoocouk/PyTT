#   Python standard library
from genericpath import isfile
import os
import sqlite3

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqliteDatabaseType import SqliteDatabaseType
from .SqliteDatabaseAddress import SqliteDatabaseAddress
from .SqliteDatabaseLock import SqliteDatabaseLock

##########
#   Public entities
@final
class SqliteDatabase(Database):

    ##########
    #   Construction
    def __init__(self,
                 address: SqliteDatabaseAddress,
                 create_new: bool):
        """
            Constructs the SqliteDatabase instance.

            @param address:
                The address of the database.
            @param create_new:
                True to create a new database, False to open an 
                already existing one.
            @raise DatabaseError:
                If the database initialization fails (usually
                due to a lock conflict).
        """
        assert isinstance(address, SqliteDatabaseAddress)
        assert isinstance(create_new, bool)

        self.__address = address
        self.__connection = None
        self.__is_open = True

        #   Obtain the lock BEFORE opening a connection
        db_path = address._SqliteDatabaseAddress__path
        lock_path = db_path + ".lock"
        try:
            self.__lock = SqliteDatabaseLock(lock_path) #   may raise DatabaseError
        except:
            connection.close()
            raise ex

        #   Lock obtained - open connection to the database
        try:
            if create_new:
                if os.path.exists(db_path):
                    raise NotImplementedError() # TODO DatabaseError
                self.__connection = sqlite3.connect(path)   # may raise any error, really
            else:
                if not os.path.isfile(db_path):
                    raise NotImplementedError() # TODO DatabaseError
                self.__connection = sqlite3.connect(path)   # may raise any error, really
        except Exception as ex:
            if self.__connection:
                self.__connection.close()
            self.__lock.close()
            raise DatabaseIoError(str(ex)) from ex

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
