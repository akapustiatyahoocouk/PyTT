#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessObject import BusinessObject
from .Exceptions import *

##########
#   Public entities
class BusinessActivityType(BusinessObject):
    """ An ActivityType in a workspace. """

    ##########
    #   Constants
    TYPE_NAME = dbapi.ActivityType.TYPE_NAME
    NAME_PROPERTY_NAME = dbapi.ActivityType.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.ActivityType.DESCRIPTION_PROPERTY_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: "Workspace", data_object: dbapi.ActivityType):
        assert isinstance(data_object, dbapi.ActivityType)
        BusinessObject.__init__(self, workspace, data_object)

    ##########
    #   BusinessObject - Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_stock_items(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def can_destroy(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_stock_items(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (properties)
    def get_name(self, credentials: Credentials) -> str:
        """
            Returns the "name" of this BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @return:
                The "name" of this BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.name
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_name(self, credentials: Credentials, new_name: str) -> None:
        """
            Sets the "name" of this BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @param new_name:
                The new "name" for this BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_name, str)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.name = new_name
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_description(self, credentials: Credentials) -> str:
        """
            Returns the "description" of this BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @return:
                The "description" of this BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.description
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_description(self, credentials: Credentials, new_description: str) -> None:
        """
            Sets the "description" of this BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @param new_description:
                The new "description" for this BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_description, str)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.description = new_description
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (associations)
    def get_activities(self, credentials: Credentials) -> Set[BusinessActivity]:
        """
            Returns the set of all BusinessActivities assigned this BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @return:
                The set of all BusinessActivities assigned this BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            result = set()
            if self.workspace.get_capabilities(credentials) is not None:
                #   The caller can see all activities
                for data_activity in self._data_object.activities:
                    result.add(self.workspace._get_business_proxy(data_activity))
            return result
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
