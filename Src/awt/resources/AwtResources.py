""" Resource definitions for "awt" component. """
#   Python standard library
from typing import final
import os
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class AwtResources(ClassWithConstants):
    """ Resources provided by the "AWT" component. """

    ##########
    #   Implementation
    __impl = FileResourceFactory(os.path.join(os.path.dirname(__file__), "Resources.txt"))

    __icon_cache: dict[str, tk.PhotoImage] = {}

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty
    def factory() -> ResourceFactory:
        """ The resource factory that provides the actual resources. """
        return AwtResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, locale: Locale = Locale.default) -> str:
        """
            Retrieves the specified string resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
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
        return AwtResources.__impl.get_string(key, locale)

    @staticmethod
    def image(key: str, locale: Locale = Locale.default) -> tk.PhotoImage:
        """
            Retrieves the specified image resource for the specified locale.
            It this cannot be done, attempts to do the same for the parent
            locale of the "locale", then for the grand-parent, etc. before
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
        return AwtResources.__impl.get_image(key, locale)
