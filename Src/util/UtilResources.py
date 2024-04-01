"""
    Resource definitions for "util" component.
"""
from typing import final

import os
import tkinter as tk

from util.Annotations import staticproperty
from util.FileResourceFactory import FileResourceFactory
from util.Locale import Locale

@final
class UtilResources:
    """ Resources provided by the "util" component. """

    __impl = FileResourceFactory(os.path.join(os.path.dirname(__file__), "resources/Resources.txt"))
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    @staticmethod
    def string(key: str, locale: Locale = Locale.default) -> str:
        return UtilResources.__impl.get_string(key, locale)

    @staticmethod
    def image(key: str, locale: Locale = Locale.default) -> tk.PhotoImage:
        return UtilResources.__impl.get_image(key, locale)
    