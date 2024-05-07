#   Python standard library
from typing import List
import re

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Capabilities import Capabilities

##########
#   Public entities
class UserValidator:
    """ An agent that "knows" hot to check various properties
        of Users in a database for validity. """

    ##########
    #   Operations
    def is_valid_enabled(self, enabled: bool) -> bool:
       return isinstance(enabled, bool)

    def is_valid_real_name(self, real_name: str) -> bool:
       return (isinstance(real_name, str) and
               (len(real_name) == len(real_name.strip())) and
               (len(real_name) > 0) and
               (len(real_name) <= 127) and
               all((ord(c) >= 32 and ord(c) != 127) for c in real_name))

    def is_valid_inactivity_timeout(self, inactivity_timeout: int) -> bool:
        if inactivity_timeout is None:
            return True
        return (isinstance(inactivity_timeout, int) and
                (inactivity_timeout > 0) and
                (inactivity_timeout < 60 * 60)) #   GUI limitation!

    def is_valid_ui_locale(self, ui_locale: Locale) -> bool:
        return (ui_locale is None) or isinstance(ui_locale, Locale)

    def is_valid_email_address(self, s: str) -> bool:
        if not isinstance(s, str):
            return False
        pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        return re.match(pattern, s) is not None

    def is_valid_email_addresses(self, email_addresses: List[str]) -> bool:
        return (isinstance(email_addresses, list) and
                all(isinstance(ea, str) for ea in email_addresses) and
                all(_is_valid_email_address(ea) for ea in email_addresses))


class AccountValidator:
    """ An agent that "knows" hot to check various properties
        of Accounts in a database for validity. """

    ##########
    #   Operations
    def is_valid_enabled(self, enabled: bool) -> bool:
       return isinstance(enabled, bool)

    def is_valid_login(self, login: str) -> bool:
       return (isinstance(login, str) and
               (len(login) == len(login.strip())) and
               (len(login) > 0) and
               (len(login) <= 127) and
               all((ord(c) >= 32 and ord(c) != 127) for c in login))

    def is_valid_password(self, password: str) -> bool:
       return isinstance(password, str)

    def is_valid_capabilities(self, capabilities: Capabilities) -> bool:
       return isinstance(capabilities, Capabilities)

    def is_valid_email_address(self, s: str) -> bool:
        if not isinstance(s, str):
            return False
        pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        return re.match(pattern, s) is not None

    def is_valid_email_addresses(self, email_addresses: List[str]) -> bool:
        return (isinstance(email_addresses, list) and
                all(isinstance(ea, str) for ea in email_addresses) and
                all(_is_valid_email_address(ea) for ea in email_addresses))


class ActivityTypeValidator:
    """ An agent that "knows" hot to check various properties
        of ActivityTypes in a database for validity. """

    ##########
    #   Operations
    def is_valid_name(self, name: str) -> bool:
       return (isinstance(name, str) and
               (len(name) == len(name.strip())) and
               (len(name) > 0) and
               (len(name) <= 127) and
               all((ord(c) >= 32 and ord(c) != 127) for c in name))

    def is_valid_description(self, description: str) -> bool:
       return (isinstance(description, str) and
               all(((ord(c) >= 32 and ord(c) != 127) or (c == "\n") or (c == "\t")) for c in description))


class Validator:
    """ An agent that "knows" how to check various properties
        of database objects for validity. """

    ##########
    #   Construction
    def __init__(self):
      self.__user = UserValidator()
      self.__account = AccountValidator()
      self.__activity_type = ActivityTypeValidator()

    ##########
    #   Properties
    @property  
    def user(self) -> UserValidator:
       """ The validator for User properties. """
       return self.__user

    @property  
    def account(self) -> AccountValidator:
       """ The validator for Account properties. """
       return self.__account

    @property  
    def activity_type(self) -> ActivityTypeValidator:
       """ The validator for ActivityType properties. """
       return self.__activity_type
