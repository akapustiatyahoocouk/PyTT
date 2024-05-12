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
class SqlPrivateActivity(SqlActivity, PrivateActivity):
    """ A private activity residing in an SQL database. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, oid: OID):
        SqlActivity.__init__(self, db, oid)
        PrivateActivity.__init__(self)

        #   Property cache
        self._fk_owner = None

    ##########
    #   DatabaseObject - Operations (life cycle)
    def destroy(self) -> None:
        self._ensure_live() #   may raise DatabaseException

        #   TODO Dis-associate from Accounts (as quick pick items)
        #   TODO Dis-associate from Events
        #   TODO Destroy associated Works
        #   TODO Dis-associate from Workloads
        #   Destroy the PrivateActivity
        try:
            self.database.begin_transaction();

            stat1 = self.database.create_statement(
                """DELETE FROM [private_activities] WHERE [pk] = ?""");
            stat1.set_int_parameter(0, self.oid)
            stat1.execute()

            stat2 = self.database.create_statement(
                """DELETE FROM [activities] WHERE [pk] = ?""");
            stat2.set_int_parameter(0, self.oid)
            stat2.execute()

            stat3 = self.database.create_statement(
                """DELETE FROM [objects] WHERE [pk] = ?""");
            stat3.set_int_parameter(0, self.oid)
            stat3.execute()

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
    #   PrivateActivity - Associations    
    @property
    def owner(self) -> User:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        return self.database._get_user_proxy(self._fk_owner)

    @owner.setter
    def owner(self, new_owner: User) -> None:
        raise NotImplementedError()

    ##########
    #   Activity - Properties

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        try:
            stat = self.database.create_statement(
                """SELECT *
                     FROM [private_activities], [activities]
                    WHERE [private_activities].[pk] = ?
                      AND [private_activities].[pk] == [activities].[pk]""");
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
            self._timeout = r["timeout", SqlDataType.INTEGER]
            self._require_comment_on_start = r["require_comment_on_start", SqlDataType.BOOLEAN]
            self._require_comment_on_finish = r["require_comment_on_finish", SqlDataType.BOOLEAN]
            self._full_screen_reminder = r["full_screen_reminder", SqlDataType.BOOLEAN]
            self._fk_activity_type = r["fk_activity_type", SqlDataType.INTEGER]
            self._fk_owner = r["fk_owner", SqlDataType.INTEGER]
        except Exception as ex:
            raise DatabaseError.wrap(ex)

