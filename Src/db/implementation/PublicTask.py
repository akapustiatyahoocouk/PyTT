#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Activity import Activity
from .PublicActivity import PublicActivity
from .Task import Task
from ..resources.DbResources import DbResources

##########
#   Public entities
class PublicTask(PublicActivity, Task):
    """ A public task in a database. """

    ##########
    #   Constants
    TYPE_NAME = "PublicTask"
    NAME_PROPERTY_NAME = Activity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = Activity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = Activity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = Activity.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = Task.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = Task.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = Task.CHILDREN_ASSOCIATION_NAME

    ##########
    #   UI traits
    @property
    def type_name(self) -> str:
        return PublicTask.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("PublicTask.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("PublicTask.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("PublicTask.LargeImage")

    ##########
    #   Associations
    @abstractproperty
    def parent(self) -> Optional[PublicTask]:
        raise NotImplementedError()

    @abstractproperty
    def children(self) -> Set[PublicTask]:
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
                    completed: bool = False) -> PublicTask:
        """
            Creates a new child PublicTask under this PublicTask.

            @param name:
                The "name" for the new PublicTask.
            @param description:
                The "description" for the new PublicTask.
            @param activity_type:
                The activity type to assign to this PublicTask or None.
            @param timeout:
                The timeout of this PublicTask, expressed in minutes, or None.
            @param require_comment_on_start:
                True if user shall be required to enter a comment
                when starting this PublicTask, else False.
            @param require_comment_on_finish:
                True if user shall be required to enter a comment
                when finishing this PublicTask, else False.
            @param full_screen_reminder:
                True if user shall be shown a full-screen reminder
                while this PublicTask is underway, else False.
            @param completed:
                True if the newly created PublicTask shall initially
                be marked as "completed", False if not.
            @return:
                The newly created PublicTask.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
