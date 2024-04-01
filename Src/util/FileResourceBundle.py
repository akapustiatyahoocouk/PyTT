from typing import Any
import tkinter as tk

from util.Locale import Locale
from util.ResourceType import ResourceType
from util.ResourceBundle import ResourceBundle

class FileResourceBundle(ResourceBundle):
    """ A resource bundle that reads resources from a text file. """
    
    ##########
    #   Construction
    def __init__(self, locale: Locale, file_name: str):
        assert isinstance(locale, Locale)
        assert isinstance(file_name, str)
        
        self.__locale = locale
        self.__file_name = file_name
        self.__resource_types: dict[str, ResourceType] = dict()
        self.__resources: dict[str, Any] = dict()
        with open(file_name) as file:
            for line in file:
                line = line.strip()
                if len(line) == 0  or line.startswith("#"):
                    continue
                print(line)
                try:
                    (key, resource_definition) = line.split("=", 1)
                    #print(key, resource_definition)
                    resource_type, resource_value = self.__prepare_resource(resource_definition)
                    #   TODO detect duplicate "key"s
                    self.__resource_types[key] = resource_type
                    self.__resources[key] = resource_value
                except Exception as ex:
                    pass    # TODO report? log?

    ##########
    #   ResourceBundle - Properties
    @property
    def locale(self) -> Locale:
        return self.__locale
        
    @property
    def keys(self) -> set[str]:
        return set(self.__resources.keys())

    ##########
    #   ResourceBundle - Operations
    def get_resource_type(self, key: str) -> ResourceType:
        assert isinstance(key, str)
        
        return self.__resource_types.get(key, ResourceType.NONE)

    def get_string(self, key: str) -> str:
        assert isinstance(key, str)
        
        result = self.__resources.get(key, None)
        if isinstance(result, str):
            return result
        raise NotImplementedError() # TODO throw KeyError!

    def get_image(self, key: str) -> tk.PhotoImage:
        assert isinstance(key, str)

        result = self.__resources.get(key, None)
        if isinstance(result, tk.PhotoImage):
            return result
        raise NotImplementedError() # TODO throw KeyError!

    ##########
    #   Implementation helpers
    def __prepare_resource(self, resource_definition: str) -> (ResourceType, Any):
        #   TODO images, etc.
        return (ResourceType.STRING, resource_definition)