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
class SqlActivityType(SqlDatabaseObject, ActivityType):
    """ An activity type residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlDatabaseObject.__init__(self, db, oid)
        ActivityType.__init__(self)

        #   Property cache
        self._name = None
        self._description = None

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        self._ensure_live()

        #   TODO Dis-associate from Activities, making these typeless
        #   Destroy the ActivityType
        try:
            self.database.begin_transaction();

            stat1 = self.database.create_statement(
                """DELETE FROM [activity_types] WHERE [pk] = ?""");
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
    #   ActivityType - Properties
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
        if not self.database.validator.activity_type.is_valid_name(new_name):
            raise InvalidDatabaseObjectPropertyError(ActivityType.TYPE_NAME, ActivityType.NAME_PROPERTY_NAME, new_name)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activity_types] SET [name] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_name)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(ActivityType.TYPE_NAME)
            self._name = new_name
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    ActivityType.NAME_PROPERTY_NAME))
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
        if not self.database.validator.activity_type.is_valid_description(new_description):
            raise InvalidDatabaseObjectPropertyError(ActivityType.TYPE_NAME, ActivityType.DESCRIPTION_PROPERTY_NAME, new_description)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activity_types] SET [description] = ? WHERE [pk] = ?""")
            stat.set_string_parameter(0, new_description)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(ActivityType.TYPE_NAME)
            self._description = new_description
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    ActivityType.DESCRIPTION_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   ActivityType - Associations
    @property
    def activities(self) -> Set[Activity]:
        self._ensure_live()

        try:
            #stat = self.database.create_statement(
            #    """SELECT [pk] FROM [accounts] WHERE [fk_user] = ?""")
            #stat.set_int_parameter(0, self.oid)
            #rs = stat.execute()
            result = set()
            #for r in rs:
            #    result.add(self.database._get_account_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        try:
            stat = self.database.create_statement(
                """SELECT * FROM [activity_types] WHERE [pk] = ?""");
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            assert len(rs) <= 1
            if len(rs) == 0:
                #   OOPS! The record is not in the database!
                self._mark_dead()
                raise DatabaseObjectDeadError(User.TYPE_NAME)
            r = rs[0]
            self._name = r["name", SqlDataType.STRING]
            self._description = r["description", SqlDataType.STRING]
        except Exception as ex:
            raise DatabaseError.wrap(ex)

