#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .BusinessActivityType import BusinessActivityType
from .BusinessPublicActivity import BusinessPublicActivity
from .BusinessTask import BusinessTask
from .Exceptions import *

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
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            try:
                result = set()
                if self.workspace.get_capabilities(credentials) is not None:
                    for data_child in self._data_object.children:
                        result.add(self.workspace._get_business_proxy(data_child))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

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
        assert isinstance(credentials, Credentials)
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert (activity_type is None) or isinstance(activity_type, BusinessActivityType)
        assert (timeout is None) or isinstance(timeout, int)
        assert isinstance(require_comment_on_start, bool)
        assert isinstance(require_comment_on_finish, bool)
        assert isinstance(full_screen_reminder, bool)
        assert isinstance(completed, bool)    

        with self.workspace:
            self._ensure_live() # may raise DatabaseError
            try:
                #   Validate parameters
                if activity_type is not None:
                    activity_type._ensure_live()
                    if activity_type.workspace is not self.workspace:
                        raise IncompatibleWorkspaceObjectError(activity_type.type_name)
                #   Validate access rights
                if not self.workspace.can_manage_public_tasks(credentials):
                    raise WorkspaceAccessDeniedError()
                #   The rest of the work is up to the DB
                data_public_task = self._data_object.create_child(
                    name=name,
                    description=description,
                    activity_type=None if activity_type is None else activity_type._data_object,
                    timeout=timeout,
                    require_comment_on_start=require_comment_on_start,
                    require_comment_on_finish=require_comment_on_finish,
                    full_screen_reminder=full_screen_reminder,
                    completed=completed);
                return self.workspace._get_business_proxy(data_public_task)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)


