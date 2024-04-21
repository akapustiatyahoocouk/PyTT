#   Python standard library
from abc import ABC, abstractmethod
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlDatabaseObject import SqlDatabaseObject

##########
#   Public entities
class SqlAccount(SqlDatabaseObject, Account):
    """ An account residing in an SQL database. """
    
    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        Account.__init__(self)

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        raise NotImplementedError()

    ##########
    #   Account - Properties
    @property
    def enabled(self) -> bool:
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        raise NotImplementedError()

    @property
    def login(self) -> str:
        raise NotImplementedError()

    @login.setter
    def login(self, new_login: str) -> None:
        raise NotImplementedError()

    @property
    def password(self) -> str:
        raise NotImplementedError()

    @password.setter
    def password(self, new_password: str) -> None:
        raise NotImplementedError()

    @property
    def password_hash(self) -> str:
        raise NotImplementedError()

    @property
    def capabilities(self) -> Capabilities:
        raise NotImplementedError()

    @capabilities.setter
    def capabilities(self, new_capabilities: Capabilities) -> None:
        raise NotImplementedError()

    @property
    def email_addresses(self) -> List[str]:
        raise NotImplementedError()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        raise NotImplementedError()

    ##########
    #   Account - Associations
    @property
    def user(self) -> User:
        raise NotImplementedError()

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        stat = self.database.create_statement(
            """SELECT * FROM accounts WHERE pk = ?""");
        stat.set_int_parameter(self.oid)
        rs = self.database.execute_sql(stat)
        pass    #   Nothing cached as DatabaseObject level
