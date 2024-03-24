""" An action that takes its properties from a ResourceFactory
    and updates these properties automatically when the 
    default Locale changes. """
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .KeyStroke import KeyStroke
from .Action import Action

class ResourceAwareAction(Action):
    """ An action that takes its properties from a ResourceFactory
        and updates these properties automatically when the default 
        Locale changes. """

    ##########
    #   Construction
    def __init__(self,
                 resource_factory: ResourceFactory,
                 resource_key_base: str):
        """
            Constructs a resource-aware action.

            @param resource_factory:
                The resource factory to use for retrieving action
                properties (such as text, etc.)
            @param resource_key_base:
                The <base> portion of the resource bunch describing
                the action. The following resources are used:
                *   <base>.Name - the action name (str, mandatory).
                *   <base>.Hotkey - the action hotkey (str, optional).
                *   <base>.Description - the action description (str, optional).
                *   <base>.Shortcut - the action shortcut (str, optional).
                *   <base>.SmallImage - the action small (16x16) image (tk.PhotoImage, optional).
                *   <base>.LargeImage - the action large (32x32) image (tk.PhotoImage, optional).
        """
        Action.__init__(self, resource_key_base)

        assert isinstance(resource_factory, ResourceFactory)
        assert isinstance(resource_key_base, str)

        self.__resource_factory = resource_factory
        self.__resource_key_base = resource_key_base
        self.__update_properties()

        Locale.add_property_change_listener(self.__update_properties)

    ##########
    #   Implementation helpers
    def __update_properties(self, *_):
        self.name = self.__load__string(self.__resource_key_base + ".Name")
        self.hotkey = self.__load_optional_string(self.__resource_key_base + ".Hotkey")
        self.description = self.__load_optional_string(self.__resource_key_base + ".Description")
        self.shortcut = self.__load_optional_keystroke(self.__resource_key_base + ".Shortcut")
        self.small_image = self.__load_optional_image(self.__resource_key_base + ".SmallImage")
        self.large_image = self.__load_optional_image(self.__resource_key_base + ".LargeImage")

    def __load__string(self, key: str) -> Optional[str]:
        return self.__resource_factory.get_string(key, Locale.default)

    def __load_optional_string(self, key: str) -> Optional[str]:
        try:
            return self.__resource_factory.get_string(key, Locale.default)
        except Exception:
            return None

    def __load_optional_image(self, key: str) -> Optional[tk.PhotoImage]:
        try:
            return self.__resource_factory.get_image(key, Locale.default)
        except Exception:
            return None

    def __load_optional_keystroke(self, key: str) -> Optional[KeyStroke]:
        try:
            s = self.__resource_factory.get_string(key, Locale.default)
            return KeyStroke.parse(s)
        except Exception:
            return None
