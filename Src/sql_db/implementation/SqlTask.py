#   Python standard library
from abc import ABC, abstractmethod
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlActivity import SqlActivity
from .SqlDataType import SqlDataType
from .SqlActivityType import SqlActivityType

##########
#   Public entities
class SqlTask(SqlActivity, Task):
    """ A task residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlActivity.__init__(self, db, oid)
        Activity.__init__(self)

        #   Property cache

    ##########
    #   Task - Properties
    @property
    def completed(self) -> bool:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self._completed

    @completed.setter
    def completed(self, new_completed: bool) -> None:
        self._ensure_live() #   may raise DatabaseException
        assert isinstance(new_completed, bool)

        #   Validate parameters
        validator = self.database.validator
        if not validator.activity.is_valid_completed(new_completed):
            raise InvalidDatabaseObjectPropertyError(Task.TYPE_NAME, Task.COMPLETED, new_completed)

        #   Make database changes
        try:
            stat = self.database.create_statement(
                """UPDATE [activities] SET [completed] = ? WHERE [pk] = ?""")
            stat.set_bool_parameter(0, new_completed)
            stat.set_int_parameter(1, self.oid)
            row_count = stat.execute()
            assert row_count <= 1
            if row_count == 0:
                #   OOPS! The database row does not exist!
                self._mark_dead()
                raise DatabaseObjectDeadError(Task.TYPE_NAME)
            self._completed = new_completed
            #   Issue notifications
            self.database.enqueue_notification(
                DatabaseObjectModifiedNotification(
                    self.database,
                    self,
                    Task.COMPLETED_PROPERTY_NAME))
        except Exception as ex:
            raise DatabaseError.wrap(ex)
