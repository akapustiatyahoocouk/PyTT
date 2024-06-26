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
from .BusinessActivity import BusinessActivity

##########
#   Public entities
class BusinessTask(BusinessActivity):
    """ A Task in a workspace. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = dbapi.Task.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.Task.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.Task.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.Task.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.Task.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.Task.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = dbapi.Task.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = dbapi.Task.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = dbapi.Task.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = dbapi.Task.CHILDREN_ASSOCIATION_NAME

    ##########
    #   Properties
    def is_completed(self, credentials: Credentials) -> bool:
        """
            Checks whether this BusinessTask is completed.

            @param credentials:
                The credentials of the service caller.
            @return:
                True if this BusinessTask is completed, False if not.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            if self.workspace.get_capabilities(credentials) == None:
                raise WorkspaceAccessDeniedError()
            try:
                return self._data_object.completed
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def set_completed(self, credentials: Credentials, new_completed: bool) -> None:
        """
            Marks this BusinessTask as completed or not.

            @param credentials:
                The credentials of the service caller.
            @param new_completed:
                True if this BusinessTask is completed, BusinessFalse if not.
            @raise DatabaseError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)
        assert isinstance(new_completed, bool)

        with self.workspace:
            self._ensure_live() # may raise WorkspaceError

            if not self.can_modify(credentials):
                raise WorkspaceAccessDeniedError()
            try:
                self._data_object.completed = new_completed
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    ##########
    #   Associations
    @abstractmethod    
    def get_parent(self, credentials: Credentials) -> Optional[BusinessTask]:
        """
            Returns the Immediate parent BusinessTask of this BusinessTask; None if none.

            @return:
                The Immediate parent BusinessTask of this BusinessTask; None if none.
            @raise WorkspaceError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod    
    def set_parent(self, credentials: Credentials, new_parent: Optional[BusinessTask]) -> None:
        """
            Sets the Immediate parent BusinessTask of this BusinessTask; None if none.

            @param new_parent:
                The new immediate parent BusinessTask for this BusinessTask; None for none.
            @raise WorkspaceError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod    
    def get_children(self, credentials: Credentials) -> Set[BusinessTask]:
        """
            Returns the set of immediate children of this BusinessTask;
            can be empty but  cannot be None or contain Nones.

            @return:
                The set of immediate children of this BusinessTask; can be
                empty but  cannot be None or contain Nones.
            @raise WorkspaceError:
                If an error occurs.
        """
        raise NotImplementedError()
