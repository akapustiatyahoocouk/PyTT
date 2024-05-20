#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Activity import Activity
from .PrivateActivity import PrivateActivity
from .Task import Task
from ..resources.DbResources import DbResources

##########
#   Private entities
class PrivateTask(PrivateActivity, Task):
    """ A private task in a database. """

    ##########
    #   Constants
    TYPE_NAME = "PrivateTask"
    NAME_PROPERTY_NAME = PrivateActivity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = PrivateActivity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = PrivateActivity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = PrivateActivity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = PrivateActivity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = PrivateActivity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = PrivateActivity.ACTIVITY_TYPE_ASSOCIATION_NAME
    OWNER_ASSOCIATION_NAME = PrivateActivity.OWNER_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = Task.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = Task.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = Task.CHILDREN_ASSOCIATION_NAME

    ##########
    #   UI traits
    @property
    def type_name(self) -> str:
        return PrivateTask.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("PrivateTask.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateTask.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateTask.LargeImage")

    ##########
    #   Associations
    @abstractproperty
    def parent(self) -> Optional[PrivateTask]:
        raise NotImplementedError()

    @abstractproperty
    def children(self) -> Set[PrivateTask]:
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    @abstractmethod
    def create_child(self,
                     name: str = None,           #   MUST specify!
                     description: str = None,    #   MUST specify!
                     activity_type: Optional[ActivityType] = None,
                     timeout: Optional[int] = None,
                     require_comment_on_start: bool = False,
                     require_comment_on_finish: bool = False,
                     full_screen_reminder: bool = False,
                     completed: bool = False) -> PrivateTask:
        """
            Creates a new child PrivateTask under this PrivateTask
            (with the same "owner" as this PrivateTask).

            @param name:
                The "name" for the new PrivateTask.
            @param description:
                The "description" for the new PrivateTask.
            @param activity_type:
                The activity type to assign to this PrivateTask or None.
            @param timeout:
                The timeout of this PrivateTask, expressed in minutes, or None.
            @param require_comment_on_start:
                True if user shall be required to enter a comment
                when starting this PrivateTask, else False.
            @param require_comment_on_finish:
                True if user shall be required to enter a comment
                when finishing this PrivateTask, else False.
            @param full_screen_reminder:
                True if user shall be shown a full-screen reminder
                while this PrivateTask is underway, else False.
            @param completed:
                True if the newly created PrivateTask shall initially
                be marked as "completed", False if not.
            @return:
                The newly created PrivateTask.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
