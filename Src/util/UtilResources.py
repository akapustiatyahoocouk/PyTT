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

    ##########
    #   Properties - PyTT version information
    @staticproperty
    def PRODUCT_ICON_SMALL() -> tk.PhotoImage:
        """ The 16x16 icon representing PyTT. """
        return UtilResources.__load_image("PyTTSmall.png")

    @staticproperty
    def PRODUCT_ICON_LARGE() -> tk.PhotoImage:
        """ The 32x32 icon representing PyTT. """
        return UtilResources.__load_image("PyTTLarge.png")

    ##########
    #   Implementation
    __icon_cache: dict[str, tk.PhotoImage] = {}
    
    @staticmethod
    def __load_image(image_name: str) -> tk.PhotoImage:
        image = UtilResources.__icon_cache.get(image_name, None)
        if image is None:
            image = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), "resources/images/" + image_name))
            UtilResources.__icon_cache[image_name] = image
        return image
    