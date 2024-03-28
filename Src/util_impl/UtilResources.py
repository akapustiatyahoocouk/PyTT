from typing import final

import os
import re
import tkinter as tk

from util_impl.Annotations import staticproperty
from util_impl.Metaclasses import ClassWithConstants

@final
class UtilResources(ClassWithConstants):
    """ Resources provided by the util package. """

    ##########    
    #   Resources requiring lazy load
    __product_icon_small = None
    __product_icon_large = None
    
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
        #   TODO kill off print(cls.__name__)
        if UtilResources.__product_icon_small is None:
            UtilResources.__product_icon_small = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), "resources/images/PyTTSmall.gif"))
        return UtilResources.__product_icon_small

    @staticproperty
    def PRODUCT_ICON_LARGE() -> tk.PhotoImage:
        """ The 32x32 icon representing PyTT. """
        #   TODO kill off print(cls.__name__)
        if UtilResources.__product_icon_large is None:
            UtilResources.__product_icon_large = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), "resources/images/PyTTLarge.gif"))
        return UtilResources.__product_icon_large
