#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
from db.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlTask import SqlTask

##########
#   Public entities
class SqlPublicTask(SqlTask, PublicTask):
    """ A public task in a SQL database. """

    ##########
    #   Constants
    TYPE_NAME = PublicTask.TYPE_NAME
    NAME_PROPERTY_NAME = PublicTask.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = PublicTask.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = PublicTask.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = PublicTask.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = PublicTask.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = PublicTask.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = PublicTask.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = PublicTask.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = PublicTask.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = PublicTask.CHILDREN_ASSOCIATION_NAME

    ##########
    #   Task - Associations
    @property
    def parent(self) -> Optional[PublicTask]:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        if self._fk_parent_task is None:
            return None
        return self.database._get_public_task_proxy(self._fk_parent_task)

    @property
    def children(self) -> Set[PublicTask]:
        self._ensure_live() #   may raise DatabaseException

        try:
            stat = self.database.create_statement(
                """SELECT [pk] FROM [activities] WHERE [fk_parent_task] = ?""")
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self.database._get_public_task_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   PublicTask - Operations (life cycle)
    def create_child(self,
                     name: str = None,           #   MUST specify!
                     description: str = None,    #   MUST specify!
                     activity_type: Optional[ActivityType] = None,
                     timeout: Optional[int] = None,
                     require_comment_on_start: bool = False,
                     require_comment_on_finish: bool = False,
                     full_screen_reminder: bool = False,
                     completed: bool = False) -> PublicTask:
        from .SqlActivityType import SqlActivityType

        self._ensure_live() # may raise DatabaseError
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert (activity_type is None) or isinstance(activity_type, SqlActivityType)
        assert (timeout is None) or isinstance(timeout, int)
        assert isinstance(require_comment_on_start, bool)
        assert isinstance(require_comment_on_finish, bool)
        assert isinstance(full_screen_reminder, bool)
        assert isinstance(completed, bool)
        
        #   Validate parameters
        validator = self.database.validator
        if not validator.activity.is_valid_name(name):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.NAME_PROPERTY_NAME, name)
        if not validator.activity.is_valid_description(description):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.DESCRIPTION_PROPERTY_NAME, description)
        if not validator.activity.is_valid_timeout(timeout):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.TIMEOUT_PROPERTY_NAME, timeout)
        if not validator.activity.is_valid_require_comment_on_start(require_comment_on_start):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.REQUIRE_COMMENT_ON_START_PROPERTY_NAME, require_comment_on_start)
        if not validator.activity.is_valid_require_comment_on_finish(require_comment_on_finish):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME, require_comment_on_finish)
        if not validator.activity.is_valid_full_screen_reminder(full_screen_reminder):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.FULL_SCREEN_REMINDER_PROPERTY_NAME, full_screen_reminder)
        if not validator.activity.is_valid_task_completed(completed):
            raise InvalidDatabaseObjectPropertyError(PublicTask.TYPE_NAME, PublicTask.COMPLETED_PROPERTY_NAME, completed)
        if activity_type is not None:
            activity_type._ensure_live()
            if activity_type.database is not self:
                raise IncompatibleDatabaseObjectError(activity_type.type_name)

        #   Make database changes
        try:
            self.database.begin_transaction();

            stat1 = self.database.create_statement(
                """INSERT INTO [objects]
                          ([object_type_name])
                          VALUES (?)""");
            stat1.set_string_parameter(0, PublicTask.TYPE_NAME)
            public_task_oid = stat1.execute()

            stat2 = self.database.create_statement(
                """INSERT INTO [activities]
                          ([pk],[name],[description],[timeout],
                           [require_comment_on_start],[require_comment_on_finish],
                           [full_screen_reminder],[fk_activity_type],
                           [completed], [fk_owner], [fk_parent_task])
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)""");
            stat2.set_int_parameter(0, public_task_oid)
            stat2.set_string_parameter(1, name)
            stat2.set_string_parameter(2, description)
            stat2.set_int_parameter(3, timeout)
            stat2.set_bool_parameter(4, require_comment_on_start)
            stat2.set_bool_parameter(5, require_comment_on_finish)
            stat2.set_bool_parameter(6, full_screen_reminder)
            stat2.set_int_parameter(7, None if activity_type is None else activity_type.oid)
            stat2.set_bool_parameter(8, completed)
            stat2.set_int_parameter(9, None)
            stat2.set_int_parameter(10, self.oid)
            stat2.execute()

            self.database.commit_transaction()
            public_task = self.database._get_public_task_proxy(public_task_oid)

            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectCreatedNotification(
                    self.database,
                    public_task))
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    PublicTask.CHILDREN_ASSOCIATION_NAME))
            if activity_type is not None:
                self.database.enqueue_notification(
                    DatabaseObjectModifiedNotification(
                        self.database,
                        activity_type,
                        ActivityType.ACTIVITIES_ASSOCIATION_NAME))

            #   Done
            return public_task
        except Exception as ex:
            self.database.rollback_transaction()
            raise DatabaseError.wrap(ex)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        SqlTask._reload_property_cache(self)
        assert isinstance(self._completed, bool)
        assert self._fk_owner is None
        assert (self._fk_parent_task is None) or isinstance(self._fk_parent_task, int)
