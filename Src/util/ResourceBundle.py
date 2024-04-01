"""
    A generic "resource bundle" provides resources for a 
    specific locale.
"""
#   Python standard library
from typing import final, Any
from abc import ABC, abstractproperty, abstractmethod
import tkinter as tk

#   Internal dependencies on modules within the same component
from util.Locale import Locale
from util.ResourceType import ResourceType

##########
#   Public entities
class ResourceBundle(ABC):
    """ A bundle of resources for a specific locale. """
    
    ##########
    #   Properties
    @abstractproperty
    def name(self) -> str:
        """ The name of this resource bundle. """
        raise NotImplementedError()

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
        raise NotImplementedError()

    @abstractmethod
    def get_resource(self, key: str) -> Any:
        """ 
            Returns the resource for the specified key.
            
            @param key:
                The key to return a resource for.
            @return:
                The resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                bundle.
         """
        raise NotImplementedError()

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
        resource = self.get_resource(key) # May throw KeyError
        if isinstance(resource, str):
            return resource
        raise KeyError("The string resource '" + key +
                        "' does not exist in " + self.name)

    def get_image(self, key: str) -> tk.PhotoImage:
        """ 
            Returns the image resource for the specified key.
            
            @param key:
                The key to return a string resource for.
            @return:
                The string resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                bundle OR the resource identified by the key is not an image.
         """
        resource = self.get_resource(key) # May throw KeyError
        if isinstance(resource, tk.PhotoImage):
            return resource
        raise KeyError("The image resource '" + key +
                        "' does not exist in " + self.name)
