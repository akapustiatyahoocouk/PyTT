"""
    Defines the Plugin Manager API.
"""
#   Python standard library
from typing import final
import os
import importlib
import traceback

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from pnp.implementation.Plugin import Plugin

##########
#   Public entities
@final
class PluginManager:
    """ The loader & manager of available plugins. """

    ##########
    #   Implementation helpers
    __discovered_plugins: set[Plugin] = set()
    __initialised_plugins: set[Plugin] = set()

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty
    def discovered_plugins() -> list[Plugin]:
        return list(PluginManager.__discovered_plugins)

    @staticproperty
    def initialised_plugins(cls) -> list[Plugin]:
        return list(PluginManager.__initialised_plugins)

    ##########
    #   Operations
    @staticmethod
    def load_plugins(root_directory: str):
        #   Discover plugins...
        PluginManager.__load_packages(root_directory, '')
        for p in Plugin.__discovered_plugins:
            PluginManager.__discovered_plugins.add(p)
        for p in PluginManager.__discovered_plugins:
            print("    Discovered plugin:", p)
        #   ...and try to initialize them
        for p in PluginManager.__discovered_plugins:
            if p not in PluginManager.__initialised_plugins:
                try:
                    p.initialize()
                    p.__initialized = True
                    PluginManager.__initialised_plugins.add(p)
                except Exception as ex:
                    #   TODO log the exception ?
                    traceback.print_exc()
                    pass

    ##########
    #   Implementation
    @staticmethod
    def __is_package_directory(directory: str) -> bool:
        entry_names = os.listdir(directory)
        for entry_name in entry_names:
            entry_path = os.path.join(directory, entry_name)
            if os.path.isfile(entry_path) and entry_name == "__init__.py":
                return True
        return False

    @staticmethod
    def __load_packages(directory: str, package_name: str):
        #print("Scanning", directory, "for packages")
        PluginManager.__load_modules(directory, package_name)

    @staticmethod
    def __load_modules(directory: str, package_name: str):
        #print("Scanning", directory, "for modules")
        entry_names = os.listdir(directory)
        for entry_name in entry_names:
            entry_path = os.path.join(directory, entry_name)
            #   TODO do not autoload the module if entry_name starts with '_'
            if (os.path.isfile(entry_path) and entry_name.endswith(".py") and
                entry_name != "__init__.py"):
                separator = "" if len(package_name) == 0 else "."
                module_name = package_name + separator + entry_name[:len(entry_name) - 3]
                #TODO kill off print("Found module", module_name)
                m = importlib.import_module(module_name)
                pass
            elif os.path.isdir(entry_path):
                separator = "" if len(package_name) == 0 else "."
                module_name = package_name + separator + entry_name
                PluginManager.__load_modules(entry_path, module_name)
