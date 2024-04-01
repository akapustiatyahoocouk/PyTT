"""
    Resource definitions for "gui" component.
"""
#   Python standard library
from typing import final, Optional
import os
import tkinter as tk

#   Dependencies on other PyTT components
from awt.api import *
from util.api import *

@final
class GuiResources(ClassWithConstants):
    """ Resources provided by the "gui" component. """

    ##########
    #   Implementation
    __icon_cache: dict[str, tk.PhotoImage] = {}

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties (Actions)
    @staticproperty
    def ACTIONS_EXIT_NAME() -> str:
        return "Exit"
    @staticproperty
    def ACTIONS_EXIT_HOTKEY() -> str:
        return "x"
    @staticproperty
    def ACTIONS_EXIT_DESCRIPTION() -> str:
        return "Exits PyTT"
    @staticproperty
    def ACTIONS_EXIT_SHORTCUT() ->Optional[KeyStroke]:
        pass    # TODO implement property
    @staticproperty
    def ACTIONS_EXIT_SMALL_IMAGE() -> str:
        return GuiResources.load_image("actions/ExitSmall.png")
    @staticproperty
    def ACTIONS_EXIT_LARGE_IMAGE() -> str:
        return GuiResources.load_image("actions/ExitLarge.png")

    @staticproperty
    def ACTIONS_ABOUT_NAME() -> str:
        return "About PyTT..."
    @staticproperty
    def ACTIONS_ABOUT_HOTKEY() -> str:
        return "b"
    @staticproperty
    def ACTIONS_ABOUT_DESCRIPTION() -> str:
        return "Shows PyTT version and copyright information"
    @staticproperty
    def ACTIONS_ABOUT_SHORTCUT() ->Optional[KeyStroke]:
        pass    # TODO implement property
    @staticproperty
    def ACTIONS_ABOUT_SMALL_IMAGE() -> str:
        return GuiResources.load_image("actions/AboutSmall.png")
    @staticproperty
    def ACTIONS_ABOUT_LARGE_IMAGE() -> str:
        return GuiResources.load_image("actions/AboutLarge.png")

    ##########
    #   Operations
    @staticmethod
    def load_image(image_name: str) -> tk.PhotoImage:
        image = GuiResources.__icon_cache.get(image_name, None)
        if image is None:
            image = tk.PhotoImage(file = os.path.join(os.path.dirname(__file__), "resources/images/" + image_name))
            GuiResources.__icon_cache[image_name] = image
        return image
    
