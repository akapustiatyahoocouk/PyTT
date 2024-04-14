"""
    Implements persistent settings of a single component.
"""
#   Python standard library
from typing import final, Optional
from configparser import ConfigParser

##########
#   Public entities
@final
class ComponentSettings:
    """ Implements persistent settings of a single component. """

    ##########
    #   Construction
    def __init__(self, config: ConfigParser, component_name: str):
        assert isinstance(component_name, str)
        assert isinstance(config, ConfigParser)

        self.__component_name = component_name
        self.__config = config
        if not config.has_section(component_name):
            config.add_section(component_name)

    ##########
    #   Operations
    def remove(self, name: str) -> None:
        assert isinstance(name, str)

        if self.__config.has_option(self.__component_name, name):
            return self.__config.remove_option(self.__component_name, name)

    def get(self, name: str, default_value: str) -> str:
        assert isinstance(name, str)
        assert isinstance(default_value, str)

        if self.__config.has_option(self.__component_name, name):
            return self.__config[self.__component_name][name]
        return default_value

    def put(self, name: str, value: str) -> None:
        assert isinstance(name, str)
        assert isinstance(value, str)

        self.__config[self.__component_name][name] = value

    def get_int(self, name: str, default_value: int) -> int:
        assert isinstance(name, str)
        assert isinstance(default_value, int)

        if self.__config.has_option(self.__component_name, name):
            try:
                return int(self.__config[self.__component_name][name])
            except ValueError:
                return default_value
        return default_value

    def put_int(self, name: str, value: int) -> None:
        assert isinstance(name, str)
        assert isinstance(value, int)

        self.__config[self.__component_name][name] = str(value)

    def get_bool(self, name: str, default_value: bool) -> bool:
        assert isinstance(name, str)
        assert isinstance(default_value, bool)

        if self.__config.has_option(self.__component_name, name):
            s = self.get(name, str(default_value))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return default_value
        return default_value

    def put_bool(self, name: str, value: bool) -> None:
        assert isinstance(name, str)
        assert isinstance(value, bool)

        self.__config[self.__component_name][name] = str(value)
