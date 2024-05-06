#   Python standard library
from typing import List, Set

#   Dependencies on other PyTT components
import db.interface.api as dbapi

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessObject import BusinessObject
from .BusinessUser import BusinessUser
from .Workspace import Workspace
from .Exceptions import *

##########
#   Public entities
class BusinessAccount(BusinessObject):
    """ An Account in a workspace. """

    ##########
    #   Constants
    TYPE_NAME = dbapi.Account.TYPE_NAME
    ENABLED_PROPERTY_NAME = dbapi.Account.ENABLED_PROPERTY_NAME
    LOGIN_PROPERTY_NAME = dbapi.Account.LOGIN_PROPERTY_NAME
    PASSWORD_PROPERTY_NAME = dbapi.Account.PASSWORD_PROPERTY_NAME
    CAPABILITIES_PROPERTY_NAME = dbapi.Account.CAPABILITIES_PROPERTY_NAME
    EMAIL_ADDRESSES_PROPERTY_NAME = dbapi.Account.EMAIL_ADDRESSES_PROPERTY_NAME
    USER_ASSOCIATION_NAME = dbapi.Account.USER_ASSOCIATION_NAME

    ##########
    #   Construction (internal only)
    def __init__(self, workspace: Workspace, data_object: dbapi.Account):
        BusinessObject.__init__(self, workspace, data_object)
    
    ##########
    #   Operations (access control)
    def can_modify(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            #   A user can modify their own details, plus anyone
            #   who can manage users can modify details of any user
            if self.workspace.can_manage_users(credentials):
                return True
            data_account = self._data_object.database.login(credentials.login, credentials._Credentials__password)
            if data_account.user == self._data_object.user:
                return True
            return False
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def can_destroy(self, credentials: Credentials) -> bool:
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        try:
            return self.workspace.can_manage_users(credentials)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (properties)
    def is_enabled(self, credentials: Credentials) -> bool:
        """
            Checks whether this BusinessAccount is enabled or disabled.
            
            @param credentials:
                The credentials of the servie caller.
            @return:
                True if this BusinessAccount is enabled, False if disabled
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
            Enables of disables this BusinessAccount.

            @param credentials:
                The credentials of the servie caller.
            @param new_enabled:
                True to enable this BusinessAccount, False to disable.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_enabled, bool)

        try:
            if self._data_object.enabled and not new_enabled:
                #   We're disabling an "enabled" account - at least
                #   one other "enabled" user must exist, with at
                #   least one "enabled" account that has ADMINISTRATOR 
                #   capabilities
                access_would_be_lost = True
                db = self.workspace._Workspace__db
                for data_user in db.users:
                    if ((not data_user.enabled) or
                        (not access_would_be_lost)):
                        continue    #   data_user cannot be a possible "admin user" OR access would not be lost
                    for data_account in data_user.accounts:
                        if ((data_account == self._data_object) or
                            (not data_account.enabled) or
                            (not data_account.capabilities.contains_all(dbapi.Capabilities.ADMINISTRATOR)) or
                            (not access_would_be_lost)):
                            continue    #   data_account cannot be a possible "admin account" OR access would not be lost
                        access_would_be_lost = False
                if access_would_be_lost:
                    raise WorkspaceAccessWouldBeLostError()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

        #   IMPORTANT: A client must have "manage users" capability
        #   to modify account's login - i.e. anyone who does NOT have
        #   that capability cannot change their own login
        if not self.workspace.can_manage_users(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.enabled = new_enabled
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_login(self, credentials: Credentials) -> str:
        """
            Returns the login of this BusinessAccount.
            
            @param credentials:
                The credentials of the servie caller.
            @return:
                The login of this BusinessAccount.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.login
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_login(self, credentials: Credentials, new_login: str) -> None:
        """
            Sets the login of this BusinessAccount.

            @param credentials:
                The credentials of the servie caller.
            @param new_login:
                The new login for this BusinessAccount.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_login, str)

        #   IMPORTANT: A client must have "manage users" capability
        #   to modify account's login - i.e. anyone who does NOT have
        #   that capability cannot change their own login
        if not self.workspace.can_manage_users(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            #   Do the work
            self._data_object.login = new_login
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_password_hash(self, credentials: Credentials) -> str:
        """
            Returns the SHA-1 hash of this BusinessAccount's password.
            The returned value is a 40-character uppercase hex string.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The SHA-1 hash of this BusinessAccount's password.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.password_hash
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_password(self, credentials: Credentials, new_password: str) -> None:
        """
            Sets the password of this BusinessAccount.

            @param credentials:
                The credentials of the servie caller.
            @param new_password:
                The new password for this BusinessAccount.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_password, str)

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.password = new_password
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_capabilities(self, credentials: Credentials) -> Capabilities:
        """
            Returns the set of capabilities of this Account.

            @param credentials:
                The credentials of the servie caller.
            @return:
                The set of capabilities of this Account.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self._data_object.capabilities
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def set_capabilities(self, credentials: Credentials, new_capabilities: Capabilities) -> None:
        """
            Sets the capabilities of this BusinessAccount.

            @param credentials:
                The credentials of the servie caller.
            @param new_capabilities:
                The new set of capabilities for this BusinessAccount.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_capabilities, Capabilities)

        #   IMPORTANT: A client must have "manage users" capability
        #   to modify account's capabilities - i.e. anyone who does NOT have
        #   that capability cannot change their own capabilities
        if not self.workspace.can_manage_users(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            #   Do the work
            self._data_object.capabilities = new_capabilities
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    def get_email_addresses(self, credentials: Credentials) -> List[str]:
        """
            Returns the list of e-mail addresses of this BusinessAccount.
            
            @param credentials:
                The credentials of the servie caller.
            @return:
                The list of e-mail addresses of this BusinessAccount;
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
            Sets the e-mail addresses of this BusinessAccount.

            @param credentials:
                The credentials of the servie caller.
            @param new_email_addresses:
                The new list of e-mail addresses for this BusinessAccount;
                cannot be None or contain Nones, but can be empty.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        assert isinstance(new_email_addresses, list)
        assert all(isinstance(a, str) for a in new_email_addresses) #   TODO properly!

        if not self.can_modify(credentials):
            raise WorkspaceAccessDeniedError()
        try:
            self._data_object.email_addresses = new_email_addresses
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (associations)
    def get_user(self, credentials: Credentials) -> Set[BusinessUser]:
        """
            Returns the BusinessUser to which this BusinessAccounts belongs.
            
            @param credentials:
                The credentials of the servie caller.
            @return:
                The BusinessUser to which this BusinessAccounts belongs.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        if self.workspace.get_capabilities(credentials) == None:
            raise WorkspaceAccessDeniedError()
        try:
            return self.workspace._get_business_proxy(self._data_object.user)
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (life cycle)
