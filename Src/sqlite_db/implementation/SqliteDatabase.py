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
from ..resources.SqliteDbResources import *

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
            self.__is_open = False
            raise ex

        #   Lock obtained - open connection to the database
        try:
            if create_new:
                if os.path.exists(db_path):
                    raise DatabaseObjectAlreadyExistsError("database", "path", db_path)
                self.__connection = sqlite3.connect(db_path, isolation_level=None)   # may raise any error, really
                init_script = SqliteDbResources.string("InitDatabaseScript")
                self.execute_script(init_script)
            else:
                if not os.path.isfile(db_path):
                    raise DatabaseObjectDoesNotExistError("database", "path", db_path)
                self.__connection = sqlite3.connect(db_path, isolation_level=None)   # may raise any error, really
                validate_script = SqliteDbResources.string("ValidateDatabaseScript")
                self.execute_script(validate_script)
        except Exception as ex:
            #TODO kill off print(traceback.format_exc())
            if self.__connection:
                self.__connection.close()
            if create_new:
                os.remove(db_path)
            self.__lock.close()
            self.__is_open = False
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
                SqlDatabase.close(self)

    ##########
    #   SqlDatabase - Overridables (database engine - specific)
    def begin_transaction(self) -> None:
        self._ensure_open() # may raise DatabaseError
        try:
            self.__connection.execute("begin")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)

    def commit_transaction(self) -> None:
        self._ensure_open() # may raise DatabaseError
        try:
            self.__connection.execute("commit")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)

    def rollback_transaction(self) -> None:
        self._ensure_open() # may raise DatabaseError
        try:
            self.__connection.execute("rollback")
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)

    def execute_sql(self, sql: str) -> None:
        self._ensure_open() # may raise DatabaseError
        assert isinstance(sql, str)

        try:
            if sql.strip().upper().startswith("INSERT"):
                cur = self.__connection.cursor()
                cur.execute(sql)
                rowid = cur.lastrowid
                cur.close()
                return rowid
            elif sql.strip().upper().startswith("SELECT"):
                cur = self.__connection.cursor()
                cur.execute(sql)
                columns = list(map(lambda d: d[0], cur.description))
                rows = cur.fetchall()
                cur.close()
                return SqlRecordSet(columns, rows)
            else:
                self.__connection.execute(sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)

