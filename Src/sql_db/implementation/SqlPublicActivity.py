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
class SqlPublicActivity(SqlActivity, PublicActivity):
    """ A public activity residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlActivity.__init__(self, db, oid)
        PublicActivity.__init__(self)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        SqlActivity._reload_property_cache(self)
        assert self._completed is None
        assert self._fk_owner is None
