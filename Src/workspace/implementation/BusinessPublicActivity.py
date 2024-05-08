#   Python standard library
from typing import Optional, List

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessActivity import BusinessActivity
from .Exceptions import *

##########
#   Public entities
class BusinessPublicActivity(BusinessActivity):
    """ A PublicActivity in a workspace. """

    ##########
    #   Constants
    TYPE_NAME = dbapi.PublicActivity.TYPE_NAME
    NAME_PROPERTY_NAME = dbapi.PublicActivity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.PublicActivity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.PublicActivity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.PublicActivity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.PublicActivity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.PublicActivity.FULL_SCREEN_REMINDER_PROPERTY_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: "Workspace", data_object: dbapi.PublicActivity):
        assert isinstance(data_object, dbapi.PublicActivity)
        BusinessActivity.__init__(self, workspace, data_object)

    ##########
    #   BusinessObject - Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_public_activities(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def can_destroy(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_public_activities(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (properties)

    ##########
    #   Operations (associations)
