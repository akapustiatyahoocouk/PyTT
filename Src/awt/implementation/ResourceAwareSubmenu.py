#   Python standard library
from typing import Optional
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from awt.implementation.Submenu import Submenu

class ResourceAwareSubmenu(Submenu):
    """ A submenu that takes its properties from a ResourceFactory
        and updates these properties automatically when the Locale
        offered by the specified LocaleProvider changes.
    """
    
    ##########
    #   Construction
    def __init__(self,
                 resource_factory: ResourceFactory,
                 locale_provider: LocaleProvider,
                 resource_key_base: str):
        """
            Constructs a resource-aware submenu.
            
            @param resource_factory:
                The resource factory to use for retrieving submenu
                properties (such as text, etc.)
            @param locale_provider:
                The locale provider that specifies the locale for
                which submenu properties are retrieved. Every time the
                locale provided by this locale provider changes, the
                submenu updates its properties automatically.
            @param resource_key_base:
                The <base> portion of the resource bunch describing 
                the submenu. The following resources are used:
                *   <base>.Label  - the submenu item text (str, mandatory).
                *   <base>.Hotkey - the submenu item hotkey (str, optional).
        """
        Submenu.__init__(self, resource_key_base)

        assert isinstance(resource_factory, ResourceFactory)
        assert isinstance(locale_provider, LocaleProvider)
        assert isinstance(resource_key_base, str)

        self.__resource_factory = resource_factory
        self.__locale_provider = locale_provider
        self.__resource_key_base = resource_key_base
        self.__update_properties()
    
    ##########
    #   Implementation helpers
    def __update_properties(self):
        self.label = self.__load__string(self.__resource_key_base + ".Label")
        self.hotkey = self.__load_optional_string(self.__resource_key_base + ".Hotkey")
        #TODO self.image
                                         
    def __load__string(self, key: str) -> Optional[str]:
        return self.__resource_factory.get_string(key, self.__locale_provider.locale)
    
    def __load_optional_string(self, key: str) -> Optional[str]:
        try:
            return self.__resource_factory.get_string(key, self.__locale_provider.locale)
        except:
            return None
