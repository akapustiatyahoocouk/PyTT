""" Resource definitions for "gui" component. """
#   Python standard library
from typing import final
import os
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

##########
#   Public entities
@final
class AdminSkinResources(ClassWithConstants):
    """ Resources provided by the "admin skin" component. """

    ##########
    #   Implementation
    __impl = FileResourceFactory(os.path.join(os.path.dirname(__file__), "Resources.txt"))

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty
    def factory() -> ResourceFactory:
        """ The resource factory that provides the actual resources. """
        return AdminSkinResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, locale: Optional[Locale] = None) -> str:
        """
            Returns a string resource from the underlying resource factory.
            
            @param key:
                The resource key.
            @param locale:
                The locale to retrieve the resource for; uses
                system default locale if not specified.
            @return
                The retrieved string resource.
            @raise KeyError:
                If the specified key does not exist in the underlying resource
                factory OR the resource identified by the key is not a string.
        """
        return AdminSkinResources.__impl.get_string(key, locale)

    @staticmethod
    def image(key: str, locale: Optional[Locale] = None) -> tk.PhotoImage:
        """
            Retyurns an image resource from the underlying resource factory.
            
            @param key:
                The resource key.
            @param locale:
                The locale to retrieve the resource for; uses
                system default locale if not specified.
            @return
                The retrieved image resource.
            @raise KeyError:
                If the specified key does not exist in the underlying resource
                factory OR the resource identified by the key is not an image.
        """
        return AdminSkinResources.__impl.get_image(key, locale)
