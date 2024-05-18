#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .BusinessPublicActivity import BusinessPublicActivity
from .BusinessTask import BusinessTask

##########
#   Public entities
class BusinessPublicTask(BusinessPublicActivity, BusinessTask):
    """ A public BusinessTask in a workspace. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = dbapi.PublicTask.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.PublicTask.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.PublicTask.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.PublicTask.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.PublicTask.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.PublicTask.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = dbapi.PublicTask.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = dbapi.PublicTask.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = dbapi.PublicTask.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = dbapi.PublicTask.CHILDREN_ASSOCIATION_NAME

    ##########
    #   Associations
    def get_parent(self, credentials: Credentials) -> Optional[BusinessPublicTask]:
        raise NotImplementedError()

    def get_children(self, credentials: Credentials) -> Set[BusinessPublicTask]:
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    def create_child(self,
                     credentials: Credentials,
                     name: str = None,           #   MUST specify!
                     description: str = None,    #   MUST specify!
                     activity_type: Optional[BusinessActivityType] = None,
                     timeout: Optional[int] = None,
                     require_comment_on_start: bool = False,
                     require_comment_on_finish: bool = False,
                     full_screen_reminder: bool = False,
                     completed: bool = False) -> BusinessPublicTask:
        """
            Creates a new child BusinessPublicTask under this BusinessPublicTask.

            @param credentials:
                The credentials of the service caller.
            @param name:
                The "name" for the new BusinessPublicTask.
            @param description:
                The "description" for the new BusinessPublicTask.
            @param activity_type:
                The activity type to assign to this BusinessPublicTask or None.
            @param timeout:
                The timeout of this BusinessPublicTask, expressed in minutes, or None.
            @param require_comment_on_start:
                True if user shall be required to enter a comment
                when starting this BusinessPublicTask, else False.
            @param require_comment_on_finish:
                True if user shall be required to enter a comment
                when finishing this BusinessPublicTask, else False.
            @param full_screen_reminder:
                True if user shall be shown a full-screen reminder
                while this BusinessPublicTask is underway, else False.
            @param completed:
                True if the newly created BusinessPublicTask shall initially
                be marked as "completed", False if not.
            @return:
                The newly created BusinessPublicTask.
            @raise WorkspaceError:
                If an error occurs.
        """
        raise NotImplementedError()


