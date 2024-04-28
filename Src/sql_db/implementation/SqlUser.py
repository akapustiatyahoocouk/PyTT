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
class SqlUser(SqlDatabaseObject, User):
    """ A user residing in an SQL database. """
    
    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        User.__init__(self)

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        raise NotImplementedError()

    ##########
    #   User - Properties
    @property
    def enabled(self) -> bool:
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        raise NotImplementedError()

    @property
    def real_name(self) -> str:
        raise NotImplementedError()

    @real_name.setter
    def real_name(self, new_real_name: str) -> None:
        raise NotImplementedError()

    @property
    def inactivity_timeout(self) -> Optional[int]:
        raise NotImplementedError()

    @inactivity_timeout.setter
    def inactivity_timeout(self, new_inactivity_timeout: Optional[int]) -> None:
        raise NotImplementedError()

    @property
    def ui_locale(self) -> Optional[Locale]:
        raise NotImplementedError()

    @ui_locale.setter
    def ui_locale(self, new_ui_locale: Optional[Locale]) -> None:
        raise NotImplementedError()

    @property
    def email_addresses(self) -> List[str]:
        raise NotImplementedError()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        raise NotImplementedError()

    ##########
    #   User - Associations
    @property
    def accounts(self) -> Set[Account]:
        raise NotImplementedError()

    ##########
    #   User - Operations (life cycle)
    def create_account(self,
                       enabled: bool = True,
                       login: str = None,  #   MUST specify!
                       password: str = "",
                       capabilities: Capabilities = Capabilities.NONE,
                       email_addresses: List[str] = []) -> Account:
        assert isinstance(enabled, bool)
        assert isinstance(login, str)
        assert isinstance(password, str)
        assert isinstance(capabilities, Capabilities)
        assert isinstance(email_addresses, list)    #   and all elements are strings
        
        #   Validate parameters (real name is valid, etc.)
        sha1 = hashlib.sha1()
        sha1.update(password.encode("utf-8"))
        password_hash = sha1.hexdigest().upper()
            
        #   Insert the relevant records into the database
        try:
            self.database.begin_transaction();
            
            stat1 = self.database.create_statement(
                """INSERT INTO objects
                          (object_type_name)
                          VALUES (?)""");
            stat1.set_string_parameter(0, Account.TYPE_NAME)
            account_oid = stat1.execute()
        
            stat2 = self.database.create_statement(
                """INSERT INTO accounts
                          (pk,
                           enabled,
                           login,
                           password_hash,
                           is_administrator,
                           can_manage_users,
                           can_manage_stock_items,
                           can_manage_beneficiaries,
                           can_manage_workloads,
                           can_manage_public_activities,
                           can_manage_public_tasks,
                           can_manage_private_activities,
                           can_manage_private_tasks,
                           can_log_work,
                           can_log_events,
                           can_generate_reports,
                           can_backup_and_restore,
                           email_addresses,
                           fk_user)
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""");
            stat2.set_int_parameter(0, account_oid)
            stat2.set_bool_parameter(1, enabled)
            stat2.set_string_parameter(2, login)
            stat2.set_string_parameter(3, password_hash)
            stat2.set_bool_parameter(4, capabilities.contains_all(Capabilities.ADMINISTRATOR))
            stat2.set_bool_parameter(5, capabilities.contains_all(Capabilities.MANAGE_USERS))
            stat2.set_bool_parameter(6, capabilities.contains_all(Capabilities.MANAGE_STOCK_ITEMS))
            stat2.set_bool_parameter(7, capabilities.contains_all(Capabilities.MANAGE_BENEFICIARIES))
            stat2.set_bool_parameter(8, capabilities.contains_all(Capabilities.MANAGE_WORKLOADS))
            stat2.set_bool_parameter(9, capabilities.contains_all(Capabilities.MANAGE_PUBLIC_ACTIVITIES))
            stat2.set_bool_parameter(10, capabilities.contains_all(Capabilities.MANAGE_PUBLIC_TASKS))
            stat2.set_bool_parameter(11, capabilities.contains_all(Capabilities.MANAGE_PRIVATE_ACTIVITIES))
            stat2.set_bool_parameter(12, capabilities.contains_all(Capabilities.MANAGE_PRIVATE_TASKS))
            stat2.set_bool_parameter(13, capabilities.contains_all(Capabilities.LOG_WORK))
            stat2.set_bool_parameter(14, capabilities.contains_all(Capabilities.LOG_EVENTS))
            stat2.set_bool_parameter(15, capabilities.contains_all(Capabilities.GENERATE_REPORTS))
            stat2.set_bool_parameter(16, capabilities.contains_all(Capabilities.BACKUP_AND_RESTORE))
            stat2.set_string_parameter(17, None if len(email_addresses) == 0 else "\n".join(email_addresses))
            stat2.set_int_parameter(18, self.oid)
            stat2.execute()

            self.database.commit_transaction()
            return self.database._get_account_proxy(account_oid)
        except Exception as ex:
            self.database.rollback_transaction()
            raise DatabaseError(str(ex)) from ex

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        stat = self.database.create_statement(
            """SELECT * FROM users WHERE pk = ?""");
        stat.set_int_parameter(self.oid)
        rs = self.database.execute_sql(stat)
        pass    #   Nothing cached as DatabaseObject level
