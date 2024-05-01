#   Python standard library
from abc import ABC, abstractmethod
import time

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDataType import SqlDataType
from .SqlDatabase import SqlDatabase

##########
#   Public entities
class SqlDatabaseObject(DatabaseObject):
    """ A generic object residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        DatabaseObject.__init__(self)

        assert isinstance(db, SqlDatabase)
        assert isinstance(oid, OID)

        assert not (oid in db._SqlDatabase__objects)
        self.__db = db
        db._SqlDatabase__objects[oid] = self

        self.__oid = oid
        self.__live = True

        #   Property cache support
        self.__property_cache_expires_at = None #   properties not cached!

    ##########
    #   DatabaseObject - Properties
    @property
    def database(self) -> Database:
        return self.__db

    @property
    def live(self) -> bool:
        return self.__oid

    @property
    def oid(self) -> OID:
        return self.__oid

    ##########
    #   Property cache support
    __PROPERTY_CACHE_TIMEOUT_SEC = 30

    def _load_property_cache(self) -> None:
        if ((self.__property_cache_expires_at is None) or
             time.time() > self.__property_cache_expires_at):
            self._reload_property_cache()   #   can raise DatabaseError
            self.__property_cache_expires_at = time.time() + SqlDatabaseObject.__PROPERTY_CACHE_TIMEOUT_SEC

    def _reload_property_cache(self) -> None:   #   Can throw DatabaseError
        pass    #   Nothing is cached as DatabaseObject level

    def _invalidate_property_cache(self) -> None:
        self.__property_cache_expires_at = None

    ##########
    #   Implementation helpers
    def _ensure_live(self) -> None:
        self.__db._ensure_open() # may raise DatabaseError
        if not self.__live:
            raise DatabaseObjectDeadError(self.type_display_name)

    def _mark_dead(self) -> None:
        self.__live = False
