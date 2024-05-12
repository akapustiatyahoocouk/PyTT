#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseObject import DatabaseObject
from .Capabilities import *
from ..resources.DbResources import DbResources

##########
#   Public entities
class Account(DatabaseObject):
    """ A user Account in a database. """

    ##########
    #   Constants
    TYPE_NAME = "Account"
    ENABLED_PROPERTY_NAME = "enabled"
    LOGIN_PROPERTY_NAME = "login"
    PASSWORD_PROPERTY_NAME = "password"
    CAPABILITIES_PROPERTY_NAME = "capabulities"
    EMAIL_ADDRESSES_PROPERTY_NAME = "emailAddresses"
    USER_ASSOCIATION_NAME = "user"

    ##########
    #   UI traits
    @property
    def display_name(self) -> str:
        try:
            return self.login
        except Exception as ex:
            return str(ex)

    @property
    def type_name(self) -> str:
        return Account.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("Account.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("Account.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("Account.LargeImage")

    ##########
    #   Properties
    @abstractproperty
    def enabled(self) -> bool:
        """
            True if this Account is enabled, False if disabled.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        """
            Enables of disables this Account.

            @param new_enabled:
                True to enable this Account, False to disable.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def login(self) -> str:
        """
            The login identifier of this Account.
            All Accounts in a database have different login identifiers.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @login.setter
    def login(self, new_login: str) -> None:
        """
            Sets the login identifier of this Account.
            All Accounts in a database must have different login identifiers.

            @param new_login:
                The new login identifier for this Account.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @property
    def password(self) -> str:
        """ Do not implement or use!!! """
        raise NotImplementedError()

    @password.setter
    def password(self, new_password: str) -> None:
        """
            Sets the password of this Account.

            @param new_password:
                The new password for this Account.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def password_hash(self) -> str:
        """
            The SHA-1 hash of this Account's password.
            The returned value is a 40-character uppercase hex string.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def capabilities(self) -> Capabilities:
        """
            The set of capabilities of this Account.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @capabilities.setter
    def capabilities(self, new_capabilities: Capabilities) -> None:
        """
            Sets the capabilities of this Account.

            @param new_capabilities:
                The new set of capabilities for this Account.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def email_addresses(self) -> List[str]:
        """
            The list of e-mail addresses of this Account;
            never None or contains Nones, but can be empty.

            The e-mail addresses of an Account complement, not replace,
            the e-mail addresses of the User who owns the Account.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        """
            Sets the e-mail addresses of this Account.

            The e-mail addresses of an Account complement, not replace,
            the e-mail addresses of the User who owns the Account.

            @param new_email_addresses:
                The new list of e-mail addresses for this Account;
                cannot be None or contain Nones, but can be empty.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def user(self) -> User:
        """
            The User to which this Account belongs.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
