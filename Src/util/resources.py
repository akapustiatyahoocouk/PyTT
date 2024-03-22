from typing import final

import tkinter as tk
import os

from util.annotations import classproperty, ReadOnlyClassConstantsMetaclass

class _ResourcesMeta(type):
    def __setattr__(cls: type, attr: str, value) -> None:
        #print(cls.__name__, attr, value)
        if re.match('^[A-Z0-9_]+$', attr):
            raise Exception('Cannot change class constant value ' + cls.__name__ + '.' + attr)
        type.__setattr__(cls, attr, value)

    @final

class Resources(metaclass=_ResourcesMeta):
    """ PyTT localisable resources. """

    ##########    
    #   Resources requiring lazy load
    __product_icon = None
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

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
        #   TODO kill off print(cls.__name__)
        if Resources.__product_icon is None:
            Resources.__product_icon = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), 'images/PyTT.gif'))
        return Resources.__product_icon
        # return tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), 'images/PyTT.gif'))
