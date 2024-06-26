#   Python standard library
from typing import Any, Optional
import os
import re
import tkinter as tk

#   Internal dependencies on modules within the same component
from util.implementation.Locale import Locale
from util.implementation.ResourceType import ResourceType
from util.implementation.ResourceFactory import ResourceFactory
from util.implementation.FileResourceBundle import FileResourceBundle

##########
#   Public entities
class FileResourceFactory(ResourceFactory):
    """ A resource factory that reads resources from a bunch
        of textual resource files related by common name pattern. """

    ##########
    #   Construction
    def __init__(self, base_resource_file_name: str):
        assert isinstance(base_resource_file_name, str)

        base_resource_file_name = os.path.abspath(base_resource_file_name)
        resource_directory = os.path.dirname(base_resource_file_name)
        resource_file_name_prefix, resource_file_name_suffix = \
            os.path.splitext(os.path.basename(base_resource_file_name))
        self.__base_resource_file_name = base_resource_file_name

        self.__resource_bundles: dict[Locale, FileResourceBundle] = dict()
        entry_names = os.listdir(resource_directory)
        for entry_name in entry_names:
            entry_path = os.path.join(resource_directory, entry_name)
            #   print(entry_path)
            if (os.path.isfile(entry_path) and
                entry_name.startswith(resource_file_name_prefix) and
                entry_name.endswith(resource_file_name_suffix)):
                #print(entry_path)
                locale_spec = entry_name[len(resource_file_name_prefix) :
                                         len(entry_name) - len(resource_file_name_suffix)]
                #print(locale_spec)
                lcv = re.search(r"^_([a-zA-Z]{2})_([a-zA-Z]{2})_(.+)", locale_spec)
                lc = re.search(r"^_([a-zA-Z]{2})_([a-zA-Z]{2})", locale_spec)
                l = re.search(r"^_([a-zA-Z]{2})", locale_spec)
                if lcv:
                    locale = Locale(lcv[1], lcv[2], lcv[3])
                elif lc:
                    locale = Locale(lc[1], lc[2])
                elif l:
                    locale = Locale(l[1])
                else:
                    locale = Locale.ROOT
                #print("Loading resource file", entry_path, "for locale", locale)
                resource_bundle = FileResourceBundle(locale, entry_path)
                self.__resource_bundles[locale] = resource_bundle

    ##########
    #   ResourceFactory - Properties
    @property
    def name(self) -> str:
        return self.__base_resource_file_name

    @property
    def supported_locales(self) -> set[Locale]:
        return set(self.__resource_bundles.keys())

    ##########
    #   ResourceFactory - Operations
    def get_resource_type(self, key: str, locale: Optional[Locale] = None) -> ResourceType:
        assert isinstance(key, str)
        assert (locale is None) or isinstance(locale, Locale)

        if locale is None:
            locale = Locale.default
        while True:
            resource_bundle = self.__resource_bundles.get(locale, None)
            if resource_bundle is not None:
                resource_type = resource_bundle.get_resource_type(key)
                if resource_type is not ResourceType.NONE:
                    return resource_type
            #   Try parent locale
            if locale == Locale.ROOT:
                #  No point in going to the next-level parent
                return ResourceType.NONE
            locale = locale.parent

    def get_resource(self, key: str, locale: Optional[Locale] = None) -> Any:
        assert isinstance(key, str)
        assert (locale is None) or isinstance(locale, Locale)

        if locale is None:
            locale = Locale.default
        while True:
            resource_bundle = self.__resource_bundles.get(locale, None)
            if resource_bundle is not None:
                try:
                    return resource_bundle.get_resource(key)
                except Exception as ex:
                    pass
            #   Try parent locale
            if locale == Locale.ROOT:
                #  No point in going to the next-level parent
                raise KeyError("The resource '" + key +
                               "' does not exist in " + self.name +
                               " or related resources")
            locale = locale.parent
