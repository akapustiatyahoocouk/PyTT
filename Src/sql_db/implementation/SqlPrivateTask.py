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
class SqlPrivateTask(SqlTask, PrivateTask):
    """ A private task in a SQL database. """

    ##########
    #   Constants
    TYPE_NAME = PrivateTask.TYPE_NAME
    NAME_PROPERTY_NAME = PrivateTask.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = PrivateTask.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = PrivateTask.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = PrivateTask.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = PrivateTask.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = PrivateTask.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = PrivateTask.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = PrivateTask.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = PrivateTask.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = PrivateTask.CHILDREN_ASSOCIATION_NAME
    OWNER_ASSOCIATION_NAME = PrivateTask.OWNER_ASSOCIATION_NAME

    ##########
    #   Task - Associations
    @property
    def parent(self) -> Optional[PrivateTask]:
        self._ensure_live() #   may raise DatabaseException

        self._load_property_cache()
        if self._fk_parent_task is None:
            return None
        return self.database._get_private_task_proxy(self._fk_parent_task)

    @property
    def children(self) -> Set[PrivateTask]:
        self._ensure_live() #   may raise DatabaseException

        try:
            stat = self.database.create_statement(
                """SELECT [pk] FROM [activities] WHERE [fk_parent_task] = ?""")
            stat.set_int_parameter(0, self.oid)
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self.database._get_private_task_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Property cache support
    def _reload_property_cache(self) -> None:
        SqlActivity._reload_property_cache(self)
        assert isinstance(self._completed, bool)
        assert isinstance(self._fk_owner, int)
        assert (self._fk_parent_task is None) or isinstance(self._fk_parent_task, int)
