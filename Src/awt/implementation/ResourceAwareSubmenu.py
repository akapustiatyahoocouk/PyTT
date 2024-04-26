""" A submenu that takes its properties from a ResourceFactory
    and updates these properties automatically when the default
    Locale changes. """
#   Python standard library
from typing import Optional

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Submenu import Submenu

class ResourceAwareSubmenu(Submenu):
    """ A submenu that takes its properties from a ResourceFactory
        and updates these properties automatically when the default
        Locale changes. """

    ##########
    #   Construction
    def __init__(self,
                 resource_factory: ResourceFactory,
                 resource_key_base: str):
        """
            Constructs a resource-aware submenu.

            @param resource_factory:
                The resource factory to use for retrieving submenu
                properties (such as text, etc.)
            @param resource_key_base:
                The <base> portion of the resource bunch describing
                the submenu. The following resources are used:
                *   <base>.Label  - the submenu item text (str, mandatory).
                *   <base>.Hotkey - the submenu item hotkey (str, optional).
        """
        Submenu.__init__(self, resource_key_base)

        assert isinstance(resource_factory, ResourceFactory)
        assert isinstance(resource_key_base, str)

        self.__resource_factory = resource_factory
        self.__resource_key_base = resource_key_base
        self.__update_properties()

        Locale.add_property_change_listener(self.__update_properties)

    ##########
    #   Implementation helpers
    def __update_properties(self, *_):
        self.label = self.__load__string(self.__resource_key_base + ".Label")
        self.hotkey = self.__load_optional_string(self.__resource_key_base + ".Hotkey")
        #TODO self.image

    def __load__string(self, key: str) -> Optional[str]:
        return self.__resource_factory.get_string(key, Locale.default)

    def __load_optional_string(self, key: str) -> Optional[str]:
        try:
            return self.__resource_factory.get_string(key, Locale.default)
        except Exception:
            return None
