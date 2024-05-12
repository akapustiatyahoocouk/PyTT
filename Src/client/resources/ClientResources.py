""" Resource definitions for "client" component. """
#   Python standard library
from typing import final, Optional
import os
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

##########
#   Public entities
@final
class ClientResources(ClassWithConstants):
    """ Resources provided by the "client" component. """

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
        return ClientResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, *args) -> str:
        result = ClientResources.__impl.get_string(key)
        if len(args) > 0:
            result = result.format(*args)
        return result

    @staticmethod
    def image(key: str) -> tk.PhotoImage:
        return ClientResources.__impl.get_image(key)
