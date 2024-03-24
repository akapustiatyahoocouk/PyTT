#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseObject import DatabaseObject
from .Account import Account
from ..resources.DbResources import DbResources

##########
#   Public entities
class User(DatabaseObject):
    """ A User in a database. """

    ##########
    #   Constants
    TYPE_NAME = "User"
    ENABLED_PROPERTY_NAME = "enabled"
    REAL_NAME_PROPERTY_NAME = "realName"
    INACTIVITY_TIMEOUT_PROPERTY_NAME = "inactivityTimeout"
    UI_LOCALE_PROPERTY_NAME = "uiLocale"
    EMAIL_ADDRESSES_PROPERTY_NAME = "emailAddresses"
    ACCOUNTS_ASSOCIATION_NAME = "accounts"

    ##########
    #   UI traits
    @property
    def display_name(self) -> str:
        try:
            return self.real_name
        except Exception as ex:
            return str(ex)

    @property
    def type_name(self) -> str:
        return User.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("User.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("User.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("User.LargeImage")

    ##########
    #   Properties
    @abstractproperty
    def enabled(self) -> bool:
        """
            True if this User is enabled, False if disabled.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        """
            Enables of disables this User.

            @param new_enabled:
                True to enable this User, False to disable.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def real_name(self) -> str:
        """
            The "real name" of this User.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @real_name.setter
    def real_name(self, new_real_name: str) -> None:
        """
            Sets the "real name" of this User.

            @param new_real_name:
                The new "real name" for this User.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def inactivity_timeout(self) -> Optional[int]:
        """
            The inactivity timeout of this User, expressed
            in minutes, or None if this user has no inactivity
            timeout.

            When a User has the "inactivity timeout" configured,
            then starts some Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @inactivity_timeout.setter
    def inactivity_timeout(self, new_inactivity_timeout: Optional[int]) -> None:
        """
            Sets the "inactivity timeout" of this User.

            When a User has the "inactivity timeout" configured,
            then starts some Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @param new_inactivity_timeout:
                The new "inactivity timeout" for this User,
                expressed in minutes, or None to remove the
                inactivity timeout from this User.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def ui_locale(self) -> Optional[Locale]:
        """
            The preferred UI locale of this User, or None if
            this user has no preferred UI locale (and will be
            therefore using the system/default UI Locale).

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @ui_locale.setter
    def ui_locale(self, new_ui_locale: Optional[Locale]) -> None:
        """
            Sets the preferred UI locale of this User.

            @param new_ui_locale:
                The new preferred UI locale for this User, or
                None to remove the preferred UI locale from this
                User (and make the User use system/default UI
                locale.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def email_addresses(self) -> List[str]:
        """
            The list of e-mail addresses of this User;
            never None or contains Nones, but can be empty.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        """
            Sets the e-mail addresses of this User.

            @param new_email_addresses:
                The new list of e-mail addresses for this User;
                cannot be None or contain Nones, but can be empty.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def accounts(self) -> Set[Account]:
        """
            The set of all Accounts of this User.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    def create_account(self,
                       enabled: bool = True,
                       login: str = None,  #   MUST specify!
                       password: str = "",
                       capabilities: Capabilities = Capabilities.NONE,
                       email_addresses: List[str] = []) -> Account:
        """
            Creates a new Account for this User.

            @param enabled:
                True to create an initially enabled Account, False
                to create an initially disabled Account.
            @param login:
                The login identifier for the new Account.
            @param password:
                The password for the new Account.
            @param capabilities:
                The capabilities for the new Account.
            @param email_addresses:
                The list of e-mail addresses for the new Account;
                cannot be None or contain Nones, but can be empty.
            @return:
                The newly created Account.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
