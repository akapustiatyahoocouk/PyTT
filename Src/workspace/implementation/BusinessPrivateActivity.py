""" A PrivateActivity in a workspace. """

#   Python standard library
from typing import Optional, List

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessActivity import BusinessActivity
from .BusinessUser import BusinessUser
from .Exceptions import *

##########
#   Public entities
class BusinessPrivateActivity(BusinessActivity):
    """ A PrivateActivity in a workspace. """

    ##########
    #   Constants
    TYPE_NAME = dbapi.PrivateActivity.TYPE_NAME
    NAME_PROPERTY_NAME = dbapi.PrivateActivity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.PrivateActivity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.PrivateActivity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.PrivateActivity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.PrivateActivity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.PrivateActivity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    OWNER_ASSOCIATION_NAME = dbapi.PrivateActivity.OWNER_ASSOCIATION_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: "Workspace", data_object: dbapi.PrivateActivity):
        assert isinstance(data_object, dbapi.PrivateActivity)
        BusinessActivity.__init__(self, workspace, data_object)

    ##########
    #   BusinessObject - Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            #   A user can modify their own private activities, plus anyone
            #   who can manage private activities can modify private activities
            #   of any user
            if self.workspace.can_manage_private_activities(credentials):
                return True
            data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
            if data_account.user == self._data_object.owner:
                return True
            return False
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def can_destroy(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            #   A user can destroy their own private activities, plus anyone
            #   who can manage private activities can destroy private activities
            #   of any user
            if self.workspace.can_manage_private_activities(credentials):
                return True
            data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
            if data_account.user == self._data_object.owner:
                return True
            return False
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (properties)

    ##########
    #   Operations (associations)
    def get_owner(self, credentials: Credentials) -> BusinessUser:
        """
            Returns the BusinessUser to which this BusinessPrivateActivity belongs.

            @return:
                The BusinessUser to which this BusinessPrivateActivity belongs.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self.workspace._get_business_proxy(self._data_object.owner)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_owner(self, credentials: Credentials, new_owner: BusinessUser) -> None:
        """
            Changes the BusinessUser to which this BusinessPrivateActivity belongs.

            @param new_owner:
                The new BusinessUser to which this BusinessPrivateActivity belongs.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_owner, BusinessUser)
        
        try:
            #   Validate parameters
            new_owner._ensure_live()
            if new_owner.workspace is not self:
                raise IncompatibleWorkspaceObjectError(new_owner.type_name)
            #   Validate access rights
            if not self.can_modify(credentials):
                raise WorkspaceAccessDeniedError()
            #   The rest of the work is up to the DB
            self._data_object.owner = new_owner._data_object
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

