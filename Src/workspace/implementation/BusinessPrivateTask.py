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
from .BusinessPrivateActivity import BusinessPrivateActivity
from .BusinessTask import BusinessTask
from .Exceptions import *

##########
#   Public entities
class BusinessPrivateTask(BusinessPrivateActivity, BusinessTask):
    """ A private BusinessTask in a workspace. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = dbapi.PrivateTask.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.PrivateTask.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.PrivateTask.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.PrivateTask.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.PrivateTask.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.PrivateTask.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = dbapi.PrivateTask.ACTIVITY_TYPE_ASSOCIATION_NAME
    OWNER_ASSOCIATION_NAME = dbapi.PrivateTask.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = dbapi.PrivateTask.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = dbapi.PrivateTask.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = dbapi.PrivateTask.CHILDREN_ASSOCIATION_NAME

    ##########
    #   BusinessObject - Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            try:
                #   A user can modify their own private tasks, plus anyone
                #   who can manage private tasks can modify private tasks
                #   of any user
                if self.workspace.can_manage_private_tasks(credentials):
                    return True
                data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
                if data_account.user == self._data_object.owner:
                    return True
                return False
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def can_destroy(self, credentials: Credentials) -> bool:
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            try:
                #   A user can destroy their own private tasks, plus anyone
                #   who can manage private tasks can destroy private tasks
                #   of any user
                if self.workspace.can_manage_private_tasks(credentials):
                    return True
                data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
                if data_account.user == self._data_object.owner:
                    return True
                return False
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    ##########
    #   Associations
    def get_parent(self, credentials: Credentials) -> Optional[BusinessPrivateTask]:
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            try:
                #   Validate access rights
                if not self.can_modify(credentials):
                    raise WorkspaceAccessDeniedError()
                if self._data_object.parent is None:
                    return None
                result = self.workspace._get_business_proxy(self._data_object.parent)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def set_parent(self, credentials: Credentials, new_parent: Optional[BusinessPublicTask]) -> None:
        assert isinstance(credentials, Credentials)
        assert (new_parent is None) or isinstance(new_parent, BusinessPublicTask)
        
        with self.workspace:
            self._ensure_live() # may raise WorkspaceError
        
            try:
                #   Validate parameters
                if new_parent is not None:
                    new_parent._ensure_live()
                    if new_parent.workspace is not self.workspace:
                        raise IncompatibleWorkspaceObjectError(new_parent.type_name)
                #   Validate access rights
                if not self.can_modify(credentials):
                    raise WorkspaceAccessDeniedError()
                #   The rest of the work is up to the DB
                self._data_object.parent = None if new_parent is None else new_parent._data_object
            except Exception as ex:
                raise WorkspaceError.wrap(ex)
                        
    def get_children(self, credentials: Credentials) -> Set[BusinessPublicTask]:
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            try:
                result = set()
                if self.can_modify(credentials):
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
                     completed: bool = False) -> BusinessPrivateTask:
        """
            Creates a new child BusinessPrivateTask under this BusinessPrivateTask.

            @param credentials:
                The credentials of the service caller.
            @param name:
                The "name" for the new BusinessPrivateTask.
            @param description:
                The "description" for the new BusinessPrivateTask.
            @param activity_type:
                The activity type to assign to this BusinessPrivateTask or None.
            @param timeout:
                The timeout of this BusinessPrivateTask, expressed in minutes, or None.
            @param require_comment_on_start:
                True if user shall be required to enter a comment
                when starting this BusinessPrivateTask, else False.
            @param require_comment_on_finish:
                True if user shall be required to enter a comment
                when finishing this BusinessPrivateTask, else False.
            @param full_screen_reminder:
                True if user shall be shown a full-screen reminder
                while this BusinessPrivateTask is underway, else False.
            @param completed:
                True if the newly created BusinessPrivateTask shall initially
                be marked as "completed", False if not.
            @return:
                The newly created BusinessPrivateTask.
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
                if not self.can_modify(credentials):
                    raise WorkspaceAccessDeniedError()
                #   The rest of the work is up to the DB
                data_private_task = self._data_object.create_child(
                    name=name,
                    description=description,
                    activity_type=None if activity_type is None else activity_type._data_object,
                    timeout=timeout,
                    require_comment_on_start=require_comment_on_start,
                    require_comment_on_finish=require_comment_on_finish,
                    full_screen_reminder=full_screen_reminder,
                    completed=completed)
                return self.workspace._get_business_proxy(data_private_task)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

