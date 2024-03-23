from abc import ABC, abstractproperty, abstractmethod

class Plugin(ABC):
    """ a generic "plugin" - an agent discovered and initialised
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
        """ The user-readable display name of this plugin. """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def initialize(self) -> None:
        """
            Called by PluginManager at mose once to initialise 
            the plugin.
            
            @raise Exception:
                If the plugin initialisation fails.
        """
        raise NotImplementedError()
