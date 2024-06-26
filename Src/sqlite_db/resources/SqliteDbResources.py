""" Resource definitions for "sqlite_db" component. """
#   Python standard library
from typing import final
import os
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class SqliteDbResources:
    """ Resources provided by the "sqlite_db" component. """

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
        return SqliteDbResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, *args) -> str:
        result = SqliteDbResources.__impl.get_string(key)
        if len(args) > 0:
            result = result.format(*args)
        return result

    @staticmethod
    def image(key: str) -> tk.PhotoImage:
        return SqliteDbResources.__impl.get_image(key)
