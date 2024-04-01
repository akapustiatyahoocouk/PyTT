"""
    A generic "resource bundle" provides resources for a 
    specific locale.
"""
from pickle import NONE
from typing import final
from abc import ABC, abstractproperty, abstractmethod
from enum import Enum

from util.Locale import Locale

@final
class ResourceType(Enum):
    NONE
    """ The resource does not exist OR its type cannot be determined. """
    
    STRING
    """ The resource is a string (str). """

    IMAGE
    """ The resource is an image (tk.PhotoImage). """
    
    #   TODO keystroke, etc.

class ResourceBundle(ABC):
    """ A bundle of resources for a specific locale. """
    
    ##########
    #   Properties
    @abstractproperty
    def locale(self) -> Locale:
        """ The Locale for which this resource bundle defines resources. """
        raise NotImplementedError()
        
    @abstractproperty
    def keys(self) -> set[str]:
        """ The set of all keys for which this resource bundle provides 
            resources (regardless of the types of these resources). """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def get_resource_type(self, key: str) -> ResourceType:
        """
            Returns the type of the specified resource.
            
            @param key:
                The key to return a string resource for.
            @return:
                The type of the resource for the specified key;
                ResourceType.NONE if the resource does not exist OR 
                its type cannot be determined.
        """

    @abstractmethod
    def get_string(self, key: str) -> str:
        """ 
            Returns the string resource for the specified key.
            
            @param key:
                The key to return a string resource for.
            @return:
                The string resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                bundle OR the resource identified by the key is not a string.
         """
        raise NotImplementedError()
