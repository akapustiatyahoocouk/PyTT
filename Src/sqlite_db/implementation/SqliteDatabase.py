#   Python standard library
from genericpath import isfile
import os
import sqlite3
import traceback

#   Dependencies on other PyTT components
from db.interface.api import *
from sql_db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqliteDatabaseType import SqliteDatabaseType
from .SqliteDatabaseAddress import SqliteDatabaseAddress
from .SqliteDatabaseLock import SqliteDatabaseLock
from sqlite_db.resources.SqliteDbResources import *

##########
#   Public entities
@final
class SqliteDatabase(SqlDatabase):

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
        SqlDatabase.__init__(self)
        
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
        except Exception as ex:
            connection.close()
            raise ex

        #   Lock obtained - open connection to the database
        try:
            if create_new:
                if os.path.exists(db_path):
                    raise AlreadyExistsError("database", "path", db_path)
                self.__connection = sqlite3.connect(db_path)   # may raise any error, really
                init_script = SqliteDbResources.string("InitDatabaseScript")
                self.execute_script(init_script)
            else:
                if not os.path.isfile(db_path):
                    raise DoesNotExistError("database", "path", db_path)
                self.__connection = sqlite3.connect(db_path)   # may raise any error, really
                validate_script = SqliteDbResources.string("ValidateDatabaseScript")
                self.execute_script(validate_script)
        except Exception as ex:
            print(traceback.format_exc())
            if self.__connection:
                self.__connection.close()
            if create_new:
                os.remove(db_path)
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
                self.__lock.close()
                self.__connection.close()
            except Exception as ex:
                raise DatabaseIoError(str(ex)) from ex
            finally:
                self.__is_open = False

    ##########
    #   SqlDatabase - Operations
    def begin_transaction(self) -> None:
        """
            Begins a new transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        try:
            self.__connection.cursor().execute("begin")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex

    def commit_transaction(self) -> None:
        """
            Commits the current transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        try:
            self.__connection.cursor().execute("commit")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex

    def rollback_transaction(self) -> None:
        """
            Rolls back the current transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        try:
            self.__connection.cursor().execute("rollback")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex

    def execute(self, sql: str) -> None:
        assert isinstance(sql, str)

        try:
            self.__connection.execute(sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex
