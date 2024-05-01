#   Python standard library
from abc import ABC, abstractmethod
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlDatabaseObject import SqlDatabaseObject
from .SqlDataType import SqlDataType

##########
#   Public entities
class SqlAccount(SqlDatabaseObject, Account):
    """ An account residing in an SQL database. """
    
    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        Account.__init__(self)
        
        #   Property cache
        self._enabled = None
        self._login = None
        self._password_hash = None
        self._capabilities = None
        self._email_addresses = None
        self._fk_user = None

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        raise NotImplementedError()

    ##########
    #   Account - Properties
    @property
    def enabled(self) -> bool:
        self._ensure_live()
        
        self._load_property_cache()
        return self._enabled

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
        self._ensure_live()
        
        self._load_property_cache()
        return self.database._get_user_proxy(self._fk_user)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        try:
            stat = self.database.create_statement(
                """SELECT * FROM accounts WHERE pk = ?""");
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            assert len(rs) <= 1
            if len(rs) == 0:
                #   OOPS! The record is not in the database!
                self._mark_dead()
                raise DatabaseObjectDeadError(Account.TYPE_NAME)
            r = rs[0]
            self._enabled = r["enabled", SqlDataType.BOOLEAN]
            self._login = r["login", SqlDataType.STRING]
            self._password_hash = r["password_hash", SqlDataType.STRING]
            self._capabilities = Capabilities.NONE
            #self._email_addresses = None
            #   Start of capability fields
            if r["is_administrator", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.ADMINISTRATOR
            if r["can_manage_users", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_USERS
            if r["can_manage_stock_items", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_STOCK_ITEMS
            if r["can_manage_beneficiaries", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_BENEFICIARIES
            if r["can_manage_workloads", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_WORKLOADS
            if r["can_manage_public_activities", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_PUBLIC_ACTIVITIES
            if r["can_manage_public_tasks", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_PUBLIC_TASKS
            if r["can_manage_private_activities", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_PRIVATE_ACTIVITIES
            if r["can_manage_private_tasks", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.MANAGE_PRIVATE_TASKS
            if r["can_log_work", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.LOG_WORK
            if r["can_log_events", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.LOG_EVENTS
            if r["can_generate_reports", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.GENERATE_REPORTS
            if r["can_backup_and_restore", SqlDataType.BOOLEAN]:
                self._capabilities |= Capabilities.BACKUP_AND_RESTORE
            #   End of capability fields
            email_addresses = r["email_addresses", SqlDataType.STRING]
            if email_addresses is None:
                self._email_addresses = []
            else:
                self._email_addresses = email_addresses.split("\n")
            self._fk_user = r["fk_user", SqlDataType.INTEGER]
        except Exception as ex:
            raise DatabaseError.wrap(ex)
