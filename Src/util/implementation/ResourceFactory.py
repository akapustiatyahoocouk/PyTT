""" Defines a "resource factory" an agent responsible
    for creation of localizable resources. """
#   Python standard library
from typing import Any, Optional
from abc import ABC, abstractmethod, abstractproperty
import tkinter as tk

#   Internal dependencies on modules within the same component
from util.implementation.Locale import Locale
from util.implementation.ResourceType import ResourceType

##########
#   Public entities
class ResourceFactory(ABC):
    """ An agent responsible for creation of localizable resources. """

    ##########
    #   Properties
    @abstractproperty
    def name(self) -> str:
        """ The name of this resource factory. """
        raise NotImplementedError()

    @abstractproperty
    def supported_locales(self) -> set[Locale]:
        """ The set of all locales supported by this resource factory. """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def get_resource_type(self, key: str, locale: Locale = Locale.default) -> ResourceType:
        """
            Returns the type of the specified resource.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
            giving up.

            @param key:
                The key to return a string resource for.
            @param locale:
                The required resource locale.
            @return:
                The type of the resource for the specified key;
                ResourceType.NONE if the resource does not exist OR
                its type cannot be determined.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_resource(self, key: str, locale: Optional[Locale] = None) -> Any:
        """
            Retrieves the specified resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
            giving up.

            @param key:
                The resource key.
            @param locale:
                The required resource locale; None == current default.
            @return:
                The resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                factory.
        """
        raise NotImplementedError()

    def get_string(self, key: str, locale: Optional[Locale] = None) -> str:
        """
            Retrieves the specified string resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
            giving up.

            @param key:
                The resource key.
            @param locale:
                The required resource locale; None == current default.
            @return:
                The string resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                factory OR the resource identified by the key is not a string.
        """
        resource = self.get_resource(key, locale)   # May throw KeyError
        if isinstance(resource, str):
            return resource
        raise KeyError("The string resource '" + key +
                       "' does not exist in " + self.name +
                       " or related resources")

    def get_image(self, key: str, locale: Optional[Locale] = None) -> tk.PhotoImage:
        """
            Retrieves the specified image resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
            giving up.

            @param key:
                The resource key.
            @param locale:
                The required resource locale; None == current default.
            @return:
                The image resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                factory OR the resource identified by the key is not a string.
        """
        resource = self.get_resource(key, locale)   # May throw KeyError
        if isinstance(resource, tk.PhotoImage):
            return resource
        raise KeyError("The image resource '" + key +
                       "' does not exist in " + self.name +
                       " or related resources")
