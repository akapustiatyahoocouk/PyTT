from abc import ABC, abstractproperty, abstractmethod

from util.Friends import FriendlyABC

class Plugin(FriendlyABC, friends=("PluginManager",)):
    """ A generic "plugin" - an agent discovered and initialised
        at origram load time. """

    ##########
    #   Implementation helpers
    __discovered_plugins = set()
    
    ##########
    #   Construction
    def __init__(self):
        Plugin.__discovered_plugins.add(self)
        self.__initialized = False
        
    ##########
    #   Properties
    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this plugin.
            IMPORTANT: 
                Base implementation throws a NotImplementedError,
                so don't call it from the overriding method
                in a concrete plugin. """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def initialize(self) -> None:
        """
            Called by PluginManager at mose once to initialise 
            the plugin.
            
            IMPORTANT: 
                Base implementation throws a NotImplementedError,
                so don't call it from the overriding method
                in a concrete plugin.
            
            @raise Exception:
                If the plugin initialisation fails.
        """
        raise NotImplementedError()
