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
        self._ensure_live() #   may raise DatabaseException

        #   TODO Dis-associate from quick pick items
        #   Destroy the Account
        try:
            user = self.user
            self.database.begin_transaction();

            stat1 = self.database.create_statement(
                """DELETE FROM [accounts] WHERE [pk] = ?""");
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
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    user,
                    User.ACCOUNTS_ASSOCIATION_NAME))

            #   Done
        except Exception as ex:
            self.database.rollback_transaction()
            raise DatabaseError.wrap(ex)

    ##########
    #   Account - Properties
    @property
    def enabled(self) -> bool:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._enabled

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_enabled, bool)

        #   Validate parameters
        validator = self.database.validator
        if not validator.account.is_valid_enabled(new_enabled):
            raise InvalidDatabaseObjectPropertyError(Account.TYPE_NAME, Account.ENABLED_PROPERTY_NAME, new_enabled)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [accounts] SET [enabled] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_enabled)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._enabled = new_enabled
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Account.ENABLED_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def login(self) -> str:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._login

    @login.setter
    def login(self, new_login: str) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_login, str)

        #   Validate parameters
        validator = self.database.validator
        if not validator.account.is_valid_login(new_login):
            raise InvalidDatabaseObjectPropertyError(Account.TYPE_NAME, Account.LOGIN_PROPERTY_NAME, new_login)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [accounts] SET [login] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_login)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._login = new_login
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Account.LOGIN_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def password(self) -> str:
        """ Don't use! Needed here because password.setter
            logic won;t work otherwise. """
        raise NotImplementedError()

    @password.setter
    def password(self, new_password: str) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_password, str)

        #   Validate parameters TODO everywhere!!!
        validator = self.database.validator
        if not validator.account.is_valid_password(new_password):
            raise InvalidDatabaseObjectPropertyError(Account.TYPE_NAME, Account.PASSWORD_PROPERTY_NAME, new_password)

        #   Make database changes
        sha1 = hashlib.sha1()
        sha1.update(new_password.encode("utf-8"))
        password_hash = sha1.hexdigest().upper()

        try:
            stat = self.database.create_statement(
                """UPDATE [accounts] SET [password_hash] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, password_hash)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._password_hash = password_hash
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Account.PASSWORD_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def password_hash(self) -> str:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._password_hash

    @property
    def capabilities(self) -> Capabilities:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._capabilities

    @capabilities.setter
    def capabilities(self, new_capabilities: Capabilities) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_capabilities, Capabilities)

        #   Validate parameters
        validator = self.database.validator
        if not validator.account.is_valid_capabilities(new_capabilities):
            raise InvalidDatabaseObjectPropertyError(Account.TYPE_NAME, Account.CAPABILITIES_PROPERTY_NAME, new_capabilities)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [accounts]
                      SET [is_administrator] = ?,
                          [can_manage_users] = ?,
                          [can_manage_stock_items] = ?,
                          [can_manage_beneficiaries] = ?,
                          [can_manage_workloads] = ?,
                          [can_manage_public_activities] = ?,
                          [can_manage_public_tasks] = ?,
                          [can_manage_private_activities] = ?,
                          [can_manage_private_tasks] = ?,
                          [can_log_work] = ?,
                          [can_log_events] = ?,
                          [can_generate_reports] = ?,
                          [can_backup_and_restore] = ?
                    WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_capabilities.contains_all(Capabilities.ADMINISTRATOR))
            stat.set_bool_parameter(1, new_capabilities.contains_all(Capabilities.MANAGE_USERS))
            stat.set_bool_parameter(2, new_capabilities.contains_all(Capabilities.MANAGE_STOCK_ITEMS))
            stat.set_bool_parameter(3, new_capabilities.contains_all(Capabilities.MANAGE_BENEFICIARIES))
            stat.set_bool_parameter(4, new_capabilities.contains_all(Capabilities.MANAGE_WORKLOADS))
            stat.set_bool_parameter(5, new_capabilities.contains_all(Capabilities.MANAGE_PUBLIC_ACTIVITIES))
            stat.set_bool_parameter(6, new_capabilities.contains_all(Capabilities.MANAGE_PUBLIC_TASKS))
            stat.set_bool_parameter(7, new_capabilities.contains_all(Capabilities.MANAGE_PRIVATE_ACTIVITIES))
            stat.set_bool_parameter(8, new_capabilities.contains_all(Capabilities.MANAGE_PRIVATE_TASKS))
            stat.set_bool_parameter(9, new_capabilities.contains_all(Capabilities.LOG_WORK))
            stat.set_bool_parameter(10, new_capabilities.contains_all(Capabilities.LOG_EVENTS))
            stat.set_bool_parameter(11, new_capabilities.contains_all(Capabilities.GENERATE_REPORTS))
            stat.set_bool_parameter(12, new_capabilities.contains_all(Capabilities.BACKUP_AND_RESTORE))
            stat.set_int_parameter(13, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._capabilities = new_capabilities
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Account.CAPABILITIES_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def email_addresses(self) -> List[str]:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._email_addresses

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_email_addresses, list)
        assert all(isinstance(a, str) for a in new_email_addresses) #   TODO properly!

        #   Validate parameters
        validator = self.database.validator
        if not validator.account.is_valid_email_addresses(new_email_addresses):
            raise InvalidDatabaseObjectPropertyError(Account.TYPE_NAME, Account.EMAIL_ADDRESSES_PROPERTY_NAME, new_email_addresses)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [accounts] SET [email_addresses] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, None if len(new_email_addresses) == 0 else "\n".join(new_email_addresses))
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            self._email_addresses = new_email_addresses
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Account.EMAIL_ADDRESSES_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Account - Associations
    @property
    def user(self) -> User:
        self._ensure_live() #   may raise DatabaseException

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
