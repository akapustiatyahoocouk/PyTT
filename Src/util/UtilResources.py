"""
    Resource definitions for "util" component.
"""
from typing import final

import os
import tkinter as tk

from util.Annotations import staticproperty
from util.Metaclasses import ClassWithConstants

@final
class UtilResources(ClassWithConstants):
    """ Resources provided by the "util" component. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties - PyTT version information
    PRODUCT_NAME = 'PyTT Time Tracker'
    """ The product name string ,"""
    
    PRODUCT_VERSION = '1.0.0 (build 20240316)'
    """ The product version string, """

    PRODUCT_COPYRIGHT = 'Copyleft (C) 2024, Andrey Kapustin'
    """ The product copyright string, """

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
    