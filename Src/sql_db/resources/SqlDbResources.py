""" Resource definitions for "sql_db" component. """

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
class SqlDbResources(ClassWithConstants):
    """ Resources provided by the "sql_db" component. """

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
        return SqlDbResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, locale: Optional[Locale] = None) -> str:
        return SqlDbResources.__impl.get_string(key, locale)

    @staticmethod
    def image(key: str, locale: Optional[Locale] = None) -> tk.PhotoImage:
        return SqlDbResources.__impl.get_image(key, locale)
