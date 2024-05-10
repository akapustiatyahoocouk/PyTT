#   Python standard library
from abc import ABC, abstractmethod
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlDatabaseObject import SqlDatabaseObject
from .SqlDataType import SqlDataType
from .SqlActivityType import SqlActivityType

##########
#   Public entities
class SqlActivity(SqlDatabaseObject, Activity):
    """ An activity residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        Activity.__init__(self)

        #   Property cache
        self._name = None
        self._description = None
        self._timeout = None
        self._require_comment_on_start = None
        self._require_comment_on_finish = None
        self._full_screen_reminder = None
        self._fk_activity_type = None

    ##########
    #   Activity - Properties
    @property
    def name(self) -> str:
        self._ensure_live()

        self._load_property_cache()
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._ensure_live()
        assert isinstance(new_name, str)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_name(new_name):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.NAME_PROPERTY_NAME, new_name)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [name] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_name)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._name = new_name
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.NAME_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def description(self) -> str:
        self._ensure_live()

        self._load_property_cache()
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._ensure_live()
        assert isinstance(new_description, str)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_description(new_description):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.DESCRIPTION_PROPERTY_NAME, new_description)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [description] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_description)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._description = new_description
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.DESCRIPTION_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def timeout(self) -> Optional[int]:
        self._ensure_live()

        self._load_property_cache()
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout: Optional[int]) -> None:
        self._ensure_live()
        assert (new_timeout is None) or isinstance(new_timeout, int)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_timeout(new_timeout):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.TIMEOUT_PROPERTY_NAME, new_timeout)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [timeout] = ? WHERE [pk] = ?""")
            stat.set_int_parameter(0, new_timeout)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._timeout = new_timeout
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.TIMEOUT_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def require_comment_on_start(self) -> bool:
        self._ensure_live()

        self._load_property_cache()
        return self._require_comment_on_start

    @require_comment_on_start.setter
    def require_comment_on_start(self, new_require_comment_on_start: bool) -> None:
        self._ensure_live()
        assert isinstance(new_require_comment_on_start, bool)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_require_comment_on_start(new_require_comment_on_start):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME, new_timeout)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [require_comment_on_start] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_require_comment_on_start)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._require_comment_on_start = new_require_comment_on_start
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def require_comment_on_finish(self) -> bool:
        self._ensure_live()

        self._load_property_cache()
        return self._require_comment_on_finish

    @require_comment_on_finish.setter
    def require_comment_on_finish(self, new_require_comment_on_finish: bool) -> None:
        self._ensure_live()
        assert isinstance(new_require_comment_on_finish, bool)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_require_comment_on_finish(new_require_comment_on_finish):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME, new_timeout)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [require_comment_on_finish] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_require_comment_on_finish)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._require_comment_on_finish = new_require_comment_on_finish
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def full_screen_reminder(self) -> bool:
        self._ensure_live()

        self._load_property_cache()
        return self._full_screen_reminder

    @full_screen_reminder.setter
    def full_screen_reminder(self, new_full_screen_reminder: bool) -> None:
        self._ensure_live()
        assert isinstance(new_full_screen_reminder, bool)

        #   Validate parameters TODO everywhere!!!
        if not self.database.validator.activity.is_valid_full_screen_reminder(new_full_screen_reminder):
            raise InvalidDatabaseObjectPropertyError(Activity.TYPE_NAME, Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME, new_timeout)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [full_screen_reminder] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_full_screen_reminder)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._full_screen_reminder = new_full_screen_reminder
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Activity - Associations
    @property
    def activity_type(self) -> Optional[ActivityType]:
        self._ensure_live()

        self._load_property_cache()
        if self._fk_activity_type is None:
            return None
        return self.database._get_activity_type_proxy(self._fk_activity_type)

    @activity_type.setter
    def activity_type(self, new_activity_type: Optional[ActivityType]) -> None:
        self._ensure_live()
        assert (new_activity_type is None) or isinstance(new_activity_type, SqlActivityType)

        #   Validate parameters
        if new_activity_type is not None:
            new_activity_type._ensure_live()
            if new_activity_type.database is not self.database:
                raise IncompatibleDatabaseObjectError(new_activity_type.type_name)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [fk_activity_type] = ? WHERE [pk] = ?""")
            stat.set_int_parameter(0, None if new_activity_type is None else new_activity_type.oid)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Activity.TYPE_NAME)
            self._fk_activity_type = None if new_activity_type is None else new_activity_type.oid
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Activity.DESCRIPTION_PROPERTY_NAME))
            if new_activity_type is not None:
                self.database.enqueue_notification(
                    DatabaseObjectModifiedNotification(
                        self.database,
                        new_activity_type,
                        ActivityType.ACTIVITIES_ASSOCIATION_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Property cache support
