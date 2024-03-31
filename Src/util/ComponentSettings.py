"""
    Implements persistent settings of a single component.
"""
from typing import final, Optional
from configparser import ConfigParser

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
    def get(name: str, default_value: str = "") -> str:    
        assert isinstance(name, str)
        assert isinstance(default_value, str)
        
        if config.has_option(self.__component_name, name):
            return self.__config[self.__component_name][name]
        return default_value    

    def put(name: str, value: str) -> str:    
        assert isinstance(name, str)
        assert isinstance(value, str)
        
        self.__config[self.__component_name][name] = value
