#   Python standard library
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
class BusinessUser(BusinessObject):
    """ A User in a workspace. """

    ##########
    #   Constants
    TYPE_NAME = dbapi.User.TYPE_NAME
    ENABLED_PROPERTY_NAME = dbapi.User.ENABLED_PROPERTY_NAME
    REAL_NAME_PROPERTY_NAME = dbapi.User.REAL_NAME_PROPERTY_NAME
    INACTIVITY_TIMEOUT_PROPERTY_NAME = dbapi.User.INACTIVITY_TIMEOUT_PROPERTY_NAME
    UI_LOCALE_PROPERTY_NAME = dbapi.User.UI_LOCALE_PROPERTY_NAME
    EMAIL_ADDRESSES_PROPERTY_NAME = dbapi.User.EMAIL_ADDRESSES_PROPERTY_NAME
    ACCOUNTS_ASSOCIATION_NAME = dbapi.User.ACCOUNTS_ASSOCIATION_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: "Workspace", data_object: dbapi.User):
        BusinessObject.__init__(self, workspace, data_object)

    ##########
    #   BusinessObject - Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            #   A user can modify their own details, plus anyone
            #   who can manage users can modify details of any user
            if self.workspace.can_manage_users(credentials):
                return True
            data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
            if data_account.user == self._data_object:
                return True
            return False
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
        raise NotImplementedError()

    def can_destroy(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_users(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   BusinessObjectOperations (life cycle)
    def destroy(self, credentials: Credentials) -> None:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            if self._data_object.enabled:
                #   We're destroying an "enabled" user - at least
                #   one other "enabled" user must exist, with at
                #   least one "enabled" account that has ADMINISTRATOR 
                #   capabilities
                access_would_be_lost = True
                db = self.workspace._Workspace__db
                for data_user in db.users:
                    if ((data_user == self._data_object) or
                        (not data_user.enabled) or
                        (not access_would_be_lost)):
                        continue    #   data_user cannot be a possible "admin user" OR access would not be lost
                    for data_account in data_user.accounts:
                        if ((not data_account.enabled) or
                            (not data_account.capabilities.contains_all(dbapi.Capabilities.ADMINISTRATOR)) or
                            (not access_would_be_lost)):
                            continue    #   data_account cannot be a possible "admin account" OR access would not be lost
                        access_would_be_lost = False
                if access_would_be_lost:
                    raise WorkspaceAccessWouldBeLostError()
            #   ...and the rest is up to the base implementation
            BusinessObject.destroy(self, credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (properties)
    def is_enabled(self, credentials: Credentials) -> bool:
        """
            Checks whether this BusinessUser is enabled or disabled.

            @param credentials:
                The credentials of the servie caller.
            @return:
                True if this BusinessUser is enabled, False if disabled
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.enabled
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_enabled(self, credentials: Credentials, new_enabled: bool) -> None:
        """
            Enables of disables this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @param new_enabled:
                True to enable this BusinessUser, False to disable.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_enabled, bool)

        try:
            if self._data_object.enabled and not new_enabled:
                #   We're disabling an "enabled" user - at least
                #   one other "enabled" user must exist, with at
                #   least one "enabled" account that has ADMINISTRATOR 
                #   capabilities
                access_would_be_lost = True
                db = self.workspace._Workspace__db
                for data_user in db.users:
                    if ((data_user == self._data_object) or
                        (not data_user.enabled) or
                        (not access_would_be_lost)):
                        continue    #   data_user cannot be a possible "admin user" OR access would not be lost
                    for data_account in data_user.accounts:
                        if ((not data_account.enabled) or
                            (not data_account.capabilities.contains_all(dbapi.Capabilities.ADMINISTRATOR)) or
                            (not access_would_be_lost)):
                            continue    #   data_account cannot be a possible "admin account" OR access would not be lost
                        access_would_be_lost = False
                if access_would_be_lost:
                    raise WorkspaceAccessWouldBeLostError()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.enabled = new_enabled
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_real_name(self, credentials: Credentials) -> str:
        """
            Returns the "real name" of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The "real name" of this BusinessUser.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.real_name
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_real_name(self, credentials: Credentials, new_real_name: str) -> None:
        """
            Sets the "real name" of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @param new_real_name:
                The new "real name" for this BusinessUser.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_real_name, str)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.real_name = new_real_name
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_inactivity_timeout(self, credentials: Credentials) -> Optional[int]:
        """
            Returns the inactivity timeout of this BusinessUser.

            When a BusinessUser has the "inactivity timeout" configured,
            then starts some Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The inactivity timeout of this BusinessUser, expressed
                in minutes, or None if this user has no inactivity
                timeout.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.inactivity_timeout
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_inactivity_timeout(self, credentials: Credentials, new_inactivity_timeout: Optional[int]) -> None:
        """
            Sets the "inactivity timeout" of this BusinessUser.

            When a BusinessUser has the "inactivity timeout" configured,
            then starts some Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @param credentials:
                The credentials of the servie caller.
            @param new_inactivity_timeout:
                The new "inactivity timeout" for this BusinessUser,
                expressed in minutes, or None to remove the
                inactivity timeout from this User.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert (new_inactivity_timeout is None) or isinstance(new_inactivity_timeout, int)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.inactivity_timeout = new_inactivity_timeout
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_ui_locale(self, credentials: Credentials) -> Optional[Locale]:
        """
            Returns the preferred UI locale of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The preferred UI locale of this BusinessUser, or None if
                this user has no preferred UI locale (and will be
                therefore using the system/default UI Locale).
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.ui_locale
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_ui_locale(self, credentials: Credentials, new_ui_locale: Optional[Locale]) -> None:
        """
            Sets the preferred UI locale of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @param new_ui_locale:
                The new preferred UI locale for this BusinessUser, or
                None to remove the preferred UI locale from this
                User (and make the User use system/default UI
                locale.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert (new_ui_locale is None) or isinstance(new_ui_locale, Locale)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.ui_locale = new_ui_locale
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_email_addresses(self, credentials: Credentials) -> List[str]:
        """
            Returns the list of e-mail addresses of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The list of e-mail addresses of this BusinessUser;
                never None or contains Nones, but can be empty.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.email_addresses
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_email_addresses(self, credentials: Credentials, new_email_addresses: List[str]) -> None:
        """
            Sets the e-mail addresses of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @param new_email_addresses:
                The new list of e-mail addresses for this BusinessUser;
                cannot be None or contain Nones, but can be empty.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        #   TODO validate new_email_addresses

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.email_addresses = new_email_addresses
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (associations)
    def get_accounts(self, credentials: Credentials) -> Set["BusinessAccount"]:
        """
            Returns the set of all BusinessAccounts of this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The set of all BusinessAccounts of this BusinessUser.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    def create_account(self,
                       credentials: Credentials,
                       enabled: bool = True,
                       login: str = None,  #   MUST specify!
                       password: str = "",
                       capabilities: Capabilities = Capabilities.NONE,
                       email_addresses: List[str] = []) -> "BusinessAccount":
        """
            Creates a new BusinessAccount for this BusinessUser.

            @param credentials:
                The credentials of the servie caller.
            @param enabled:
                True to create an initially enabled BusinessAccount, False
                to create an initially disabled BusinessAccount.
            @param login:
                The login identifier for the new BusinessAccount.
            @param password:
                The password for the new BusinessAccount.
            @param capabilities:
                The capabilities for the new BusinessAccount.
            @param email_addresses:
                The list of e-mail addresses for the new BusinessAccount;
                cannot be None or contain Nones, but can be empty.
            @return:
                The newly created BusinessAccount.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(enabled, bool)
        assert isinstance(login, str)
        assert isinstance(password, str)
        assert isinstance(capabilities, Capabilities)
        assert isinstance(email_addresses, list)    #   and all elements are strings
        raise NotImplementedError()
