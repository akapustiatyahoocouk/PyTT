"""
    Implementa persistent settings.
"""
#   Python standard library
from typing import final
from pathlib import Path
import os
import atexit
from configparser import ConfigParser

#   Internal dependencies on modules within the same component
from util.implementation.ComponentSettings import ComponentSettings

##########
#   Implementation helpers (persistence)
_config_directory = os.path.join(Path.home(), ".PyTT")
Path(_config_directory).mkdir(parents=True, exist_ok=True)

_config_file_name = os.path.join(_config_directory, "config.ini")
_config = ConfigParser()
_config.read(_config_file_name)

def _exit_handler():
    try:
        with open(_config_file_name, "w") as configfile:
            _config.write(configfile)
    except:
        pass    #   TODO log ?
atexit.register(_exit_handler)

##########
#   Public entities
@final
class Settings:
    """ Persistent settings. """

    ##########
    #   Implementation
    __component_settings: dict[str, ComponentSettings] = {}

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Operations
    @staticmethod
    def get(component_name: str) -> ComponentSettings:
        assert isinstance(component_name, str)

        component_settings = Settings.__component_settings.get(component_name, None)
        if component_settings is None:
            component_settings = ComponentSettings(_config, component_name)
            Settings.__component_settings[component_name] = component_settings
        return component_settings
