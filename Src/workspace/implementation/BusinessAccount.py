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
    def can_destroy(self, credentials: Credentials) -> bool:
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        #   TODO validate new_email_addresses
        raise NotImplementedError()

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
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
