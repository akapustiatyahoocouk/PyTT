from types import NoneType
from typing import Any, final

import tkinter as tk
import os

from util.annotations import classproperty, ReadOnlyClassConstantsMetaclass

@final
class UtilResources(metaclass = ReadOnlyClassConstantsMetaclass):
    """ Resources provided by the util pckage. """
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False

    ##########
    #   Properties - PyTT version information
    PRODUCT_NAME = 'PyTT Time Tracker'
    """ The product name string ,"""
    
    PRODUCT_VERSION = '1.0.0 (build 20240316)'
    """ The product version string, """

    PRODUCT_COPYRIGHT = 'Copyleft (C) 2024, Andrey Kapustin'
    """ The product copyright string, """

    @classproperty
    def PRODUCT_ICON(cls) -> tk.PhotoImage:
        """ The 32x32 icon representing PyTT. """
        print(cls.__name__)
        if not hasattr(UtilResources, '_UtilResources__product_icon'):
            UtilResources._UtilResources__product_icon = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), 'images/PyTT.gif'))
        return UtilResources._UtilResources__product_icon
