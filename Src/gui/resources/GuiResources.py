""" Resource definitions for "gui" component. """
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
class GuiResources(ClassWithConstants):
    """ Resources provided by the "gui" component. """

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
        return GuiResources.__impl

    ##########
    #   Operations
    @staticmethod
    def string(key: str, locale: Locale = Locale.default) -> str:
        return GuiResources.__impl.get_string(key, locale)

    @staticmethod
    def image(key: str, locale: Locale = Locale.default) -> tk.PhotoImage:
        return GuiResources.__impl.get_image(key, locale)
