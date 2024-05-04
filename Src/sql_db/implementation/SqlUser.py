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
class SqlUser(SqlDatabaseObject, User):
    """ A user residing in an SQL database. """
    
    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        User.__init__(self)

        #   Property cache
        self._enabled = None
        self._real_name = None
        self._inactivity_timeout = None
        self._ui_locale = None
        self._email_addresses = None

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        self._ensure_live()
        
        #   TODO Destroy associated Events
        #   TODO Destroy associated Works
        #   TODO Destroy associated PrivateActivities (including PrivateTasks)
        #   Destroy associated Accounts
        for account in self.accounts:
            account.destroy()
        #   Destroy the User
        try:
            self.database.begin_transaction();
            
            stat1 = self.database.create_statement(
                """DELETE FROM [users] WHERE [pk] = ?""");
            stat1.set_int_parameter(0, self.oid)
            stat1.execute()
        
            stat2 = self.database.create_statement(
                """DELETE FROM [objects] WHERE [pk] = ?""");
            stat2.set_int_parameter(0, self.oid)
            stat2.execute()

            self.database.commit_transaction()
            self._mark_dead()
            
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectDestroyedNotification(
                    self.database, 
                    self))
            
            #   Done
        except Exception as ex:
            self.database.rollback_transaction()
            raise DatabaseError.wrap(ex)

    ##########
    #   User - Properties
    @property
    def enabled(self) -> bool:
        self._ensure_live()
        
        self._load_property_cache()
        return self._enabled

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        self._ensure_live()
        assert isinstance(new_enabled, bool)
        
        try:        
            stat = self.database.create_statement(
                """UPDATE [users] SET [enabled] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_enabled)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._enabled = new_enabled
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def real_name(self) -> str:
        self._ensure_live()
        
        self._load_property_cache()
        return self._real_name

    @real_name.setter
    def real_name(self, new_real_name: str) -> None:
        self._ensure_live()
        assert isinstance(new_real_name, str)
        
        try:        
            stat = self.database.create_statement(
                """UPDATE [users] SET [real_name] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_real_name)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._real_name = new_real_name
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def inactivity_timeout(self) -> Optional[int]:
        self._ensure_live()
        
        self._load_property_cache()
        return self._inactivity_timeout

    @inactivity_timeout.setter
    def inactivity_timeout(self, new_inactivity_timeout: Optional[int]) -> None:
        self._ensure_live()
        assert (new_inactivity_timeout is None) or isinstance(new_inactivity_timeout, int)
        
        try:        
            stat = self.database.create_statement(
                """UPDATE [users] SET [inactivity_timeout] = ? WHERE [pk] = ?""")
            stat.set_int_parameter(0, new_inactivity_timeout)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._inactivity_timeout = new_inactivity_timeout
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def ui_locale(self) -> Optional[Locale]:
        self._ensure_live()
        
        self._load_property_cache()
        return self._ui_locale

    @ui_locale.setter
    def ui_locale(self, new_ui_locale: Optional[Locale]) -> None:
        self._ensure_live()
        assert (new_ui_locale is None) or isinstance(new_ui_locale, Locale)
        
        try:        
            stat = self.database.create_statement(
                """UPDATE [users] SET [ui_locale] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, None if new_ui_locale is None else repr(new_ui_locale))
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._ui_locale = new_ui_locale
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def email_addresses(self) -> List[str]:
        self._ensure_live()
        
        self._load_property_cache()
        return self._email_addresses.copy()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        self._ensure_live()
        assert isinstance(new_email_addresses, list)
        assert all(isinstance(a, str) for a in new_email_addresses) #   TODO properly!
        
        try:        
            stat = self.database.create_statement(
                """UPDATE [users] SET [email_addresses] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, None if len(new_email_addresses) == 0 else "|".join(new_email_addresses))
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._email_addresses = new_email_addresses
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   User - Associations
    @property
    def accounts(self) -> Set[Account]:
        self._ensure_live()
        
        try:        
            stat = self.database.create_statement(
                """SELECT [pk] FROM [accounts] WHERE [fk_user] = ?""")
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self.database._get_account_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

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
            account = self.database._get_account_proxy(account_oid)
            
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectCreatedNotification(
                    self.database, 
                    account))
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database, 
                    self,
                    User.ACCOUNTS_ASSOCIATION_NAME))
            #   TODO
            
            #   Done
            return account
        except Exception as ex:
            self.database.rollback_transaction()
            raise DatabaseError.wrap(ex)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        try:
            stat = self.database.create_statement(
                """SELECT * FROM users WHERE pk = ?""");
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            assert len(rs) <= 1
            if len(rs) == 0:
                #   OOPS! The record is not in the database!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            r = rs[0]
            self._enabled = r["enabled", SqlDataType.BOOLEAN]
            self._real_name = r["real_name", SqlDataType.STRING]
            self._inactivity_timeout = r["inactivity_timeout", SqlDataType.INTEGER]
            ui_locale_name = r["ui_locale", SqlDataType.STRING]
            self._ui_locale = None if ui_locale_name is None else Locale.parse(ui_locale_name)
            email_addresses = r["email_addresses", SqlDataType.STRING]
            if email_addresses is None:
                self._email_addresses = []
            else:
                self._email_addresses = email_addresses.split("|")
        except Exception as ex:
            raise DatabaseError.wrap(ex)

