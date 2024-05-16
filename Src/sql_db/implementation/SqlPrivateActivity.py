#   Python standard library
from abc import ABC, abstractmethod
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *
from .SqlActivity import SqlActivity

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlDatabaseObject import SqlDatabaseObject
from .SqlDataType import SqlDataType

##########
#   Public entities
class SqlPrivateActivity(SqlActivity, PrivateActivity):
    """ A private activity residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlActivity.__init__(self, db, oid)
        PrivateActivity.__init__(self)

    ##########
    #   PrivateActivity - Associations    
    @property
    def owner(self) -> User:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self.database._get_user_proxy(self._fk_owner)

    @owner.setter
    def owner(self, new_owner: User) -> None:
        raise NotImplementedError()

    ##########
    #   Activity - Properties

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        SqlActivity._reload_property_cache(self)
        assert self._completed is None
        assert isinstance(self._fk_owner, int)
        assert self._fk_parent_task is None
        