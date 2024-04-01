"""
    Defines a "resource factory" an agent responsible
    for creation of localizable resources.
"""
from abc import ABC, abstractmethod, abstractproperty
import tkinter as tk

from util.Locale import Locale

class ResourceFactory(ABC):
    """ An agent responsible for creation of localizable resources. """
    
    ##########
    #   Properties
    @abstractproperty
    def supported_locales() -> set[Locale]:
        """ The set of all locales supported by this resource factory. """
        raise NotImplementedError()
        
    ##########
    #   Operations
    @abstractmethod
    def get_string(self, key: str, locale: Locale = Locale.default) -> str:
        """ 
            Retrieves the specified string resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of rht "locale", then for the grand-parent, etc. before
            giving up.
            
            @param key:
                The resource key.
            @param locale:
                The required resource locale.
            @return:
                The string resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                factory OR the resource identified by the key is not a string.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image(self, key: str, locale: Locale = Locale.default) -> tk.PhotoImage:
        """ 
            Retrieves the specified image resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of rht "locale", then for the grand-parent, etc. before
            giving up.
            
            @param key:
                The resource key.
            @param locale:
                The required resource locale.
            @return:
                The image resource for the specified key.
            @raise KeyError:
                If the specified key does not exist in this resource
                factory OR the resource identified by the key is not a string.
        """
        raise NotImplementedError()
