""" Resource definitions for "util" component. """

#   Python standard library
from typing import final, Optional

import os
import tkinter as tk

#   Internal dependencies on modules within the same component
from util.implementation.Annotations import staticproperty
from util.implementation.ResourceFactory import ResourceFactory
from util.implementation.FileResourceFactory import FileResourceFactory
from util.implementation.Locale import Locale

##########
#   Public entities
@final
class UtilResources:
    """ Resources provided by the "util" component. """

    __impl = FileResourceFactory(os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "resources/Resources.txt"))
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty
    def factory() -> ResourceFactory:
        """ The resource factory that provides the actual resources. """
        return UtilResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, *args) -> str:
        result = UtilResources.__impl.get_string(key)
        if len(args) > 0:
            result = result.format(*args)
        return result

    @staticmethod
    def image(key: str) -> tk.PhotoImage:
        return UtilResources.__impl.get_image(key)
    