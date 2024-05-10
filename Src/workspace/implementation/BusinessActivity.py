#   Python standard library
from typing import Optional, List

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessObject import BusinessObject
from .BusinessActivityType import BusinessActivityType
from .Exceptions import *

##########
#   Public entities
class BusinessActivity(BusinessObject):
    """ An Activity in a workspace. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = dbapi.Activity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = dbapi.Activity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = dbapi.Activity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = dbapi.Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = dbapi.Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = dbapi.Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = dbapi.Activity.ACTIVITY_TYPE_ASSOCIATION_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: "Workspace", data_object: dbapi.Activity):
        assert isinstance(data_object, dbapi.Activity)
        BusinessObject.__init__(self, workspace, data_object)

    ##########
    #   Operations (properties)
    def get_name(self, credentials: Credentials) -> str:
        """
            Returns the "name" of this BusinessActivity.

            @param credentials:
                The credentials of the service caller.
            @return:
                The "name" of this BusinessActivity.
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
            Sets the "name" of this BusinessActivity.

            @param credentials:
                The credentials of the service caller.
            @param new_name:
                The new "name" for this BusinessActivity.
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
            Returns the "description" of this BusinessActivity.

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
            Sets the "description" of this BusinessActivity.

            @param credentials:
                The credentials of the service caller.
            @param new_description:
                The new "description" for this BusinessActivity.
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

    def get_timeout(self, credentials: Credentials) -> Optional[int]:
        """
            Returns the "timeout" of this BusinessActivity.

            When an BusinessActivity has the "timeout" configured, then when a
            user starts that BusinessActivity and does nothing at all for
            that period of time, the BusinessActivity ends automatically.

            @param credentials:
                The credentials of the service caller.
            @return:
                The timeout of this BusinessActivity, expressed in minutes, or
                None if this BusinessActivity has no timeout.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.timeout
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_timeout(self, credentials: Credentials, new_timeout: Optional[int]) -> None:
        """
            Sets the "timeout" of this BusinessActivity.

            When a BusinessActivity has the "timeout" configured, then when a
            user starts that BusinessActivity and does nothing at all for
            that period of time, the BusinessActivity ends automatically.

            @param credentials:
                The credentials of the service caller.
            @param new_timeout:
                The new "timeout" for this BusinessActivity, expressed in minutes,
                or None to remove the timeout from this BusinessActivity.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert (new_timeout is None) or isinstance(new_timeout, int)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.timeout = new_timeout
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_require_comment_on_start(self, credentials: Credentials) -> bool:
        """
            Checks whether a user is required to make a comment when starting
            this BusinessActivity. These comments are recorded as
            Events in the database.

            @param credentials:
                The credentials of the service caller.
            @return:
                True if a user is required to make a comment when starting
                this BusinessActivity, False if not. These comments are recorded as
                Events in the database.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.require_comment_on_start
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_require_comment_on_start(self, credentials: Credentials, new_require_comment_on_start: bool) -> None:
        """
            Specifies whether a user is required to make a comment when
            starting this BusinessActivity. These comments are recorded as Events
            in the database.

            @param credentials:
                The credentials of the service caller.
            @param new_require_comment_on_start:
                True to mark this BusinessActivity as requiring a comment whan a
                user starts it, False to make this BusinessActivity not require
                a user comment when starting it.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_require_comment_on_start, bool)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.require_comment_on_start = new_require_comment_on_start
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_require_comment_on_finish(self, credentials: Credentials) -> bool:
        """
            Checks whether a user is required to make a comment when finishing
            this BusinessActivity. These comments are recorded as
            Events in the database.

            @param credentials:
                The credentials of the service caller.
            @return:
                True if a user is required to make a comment when finishing
                this BusinessActivity, False if not. These comments are recorded as
                Events in the database.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.require_comment_on_finish
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
    
    def set_require_comment_on_finish(self, credentials: Credentials, new_require_comment_on_finish: bool) -> None:
        """
            Specifies whether a user is required to make a comment when
            finishing this BusinessActivity. These comments are recorded as Events
            in the database.

            @param credentials:
                The credentials of the service caller.
            @param new_require_comment_on_finish:
                True to mark this BusinessActivity as requiring a comment whan a
                user finishes it, False to make this BusinessActivity not require
                a user comment when finishing it.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_require_comment_on_finish, bool)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.require_comment_on_finish = new_require_comment_on_finish
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_full_screen_reminder(self, credentials: Credentials) -> bool:
        """
            Checks whether a user shall see a full-screen reminder when this 
            BusinessActivity, so that the user is reminded to "end" the 
            BusinessActivitywhen starting on something else.

            @param credentials:
                The credentials of the service caller.
            @return:
                True if a user shall see a full-screen reminder when this BusinessActivity 
                is underway (useful for activities such as "in a meeting", "on a 
                lunch break", etc.), so that the user is reminded to "end" the 
                BusinessActivity when starting on something else.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.full_screen_reminder
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
            
    def set_full_screen_reminder(self, credentials: Credentials, new_full_screen_reminder: bool) -> None:
        """
            True if a user shall see a full-screen reminder when this BusinessActivity 
            is underway (useful for activities such as "in a meeting", "on a 
            lunch break", etc.), so that the user is reminded to "end" the 
            Activity when starting on something else.

            @param credentials:
                The credentials of the service caller.
            @param new_full_screen_reminder:
                True to mark this BusinessActivity as providing a full-screen reminder
                to the user when the BusinessActivity is underway, False to not privide
                such full-screen reminder when the BusinessActivity is underway.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_full_screen_reminder, bool)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.full_screen_reminder = new_full_screen_reminder
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (associations)
    def get_activity_type(self, credentials: Credentials) -> Optional["BusinessActivityType"]:
        """
            Returns the BusinessActivityType assigned to this BusinessActivity, 
            None if this BusinessActivity is not assigned an BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @return:
                The BusinessActivityType assigned to this BusinessActivity, None 
                if this BusinessActivity is not assigned an BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            result = None
            if self.workspace.get_capabilities(credentials) is not None:
                #   The caller can see all activity types
                if self._data_object.activity_type is None:
                    return None
                result = self.workspace._get_business_proxy(self._data_object.activity_type)
            return result
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_activity_type(self, credentials: Credentials, new_activity_type: Optional["BusinessActivityType"]) -> None:
        """
            Sets the BusinessActivityType assigned to this BusinessActivity.

            @param credentials:
                The credentials of the service caller.
            @param new_activity_type:
                The new BusinessActivityType to assign to this BusinessActivity,
                None to set the BusinessActivity with no assigned BusinessActivityType.
            @return:
                The BusinessActivityType assigned to this BusinessActivity, None 
                if this BusinessActivity is not assigned an BusinessActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert (new_activity_type is None) or isinstance(new_activity_type, BusinessActivityType)
        
        try:
            #   Validate parameters
            if new_activity_type is not None:
                new_activity_type._ensure_live()
                if new_activity_type.workspace is not self:
                    raise IncompatibleWorkspaceObjectError(new_activity_type.type_name)
            #   Validate access rights
            if not self.can_modify(credentials):
                raise WorkspaceAccessDeniedError()
            #   The rest of the work is up to the DB
            self._data_object.activity_type = None if new_activity_type is None else new_activity_type._data_object
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

