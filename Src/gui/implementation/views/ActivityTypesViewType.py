#   Python standard library
from typing import final
from abc import ABC, abstractmethod, abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .View import View
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class ActivityTypesViewType(ViewType):

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : ViewType = None

    def __init__(self):
        assert ActivityTypesViewType.__instance_acquisition_in_progress, "Use ActivityTypesViewType.instance() instead"
        ViewType.__init__(self)

    @staticproperty
    def instance() -> ViewType:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if ActivityTypesViewType.__instance is None:
            ActivityTypesViewType.__instance_acquisition_in_progress = True
            ActivityTypesViewType.__instance = ActivityTypesViewType()
            ActivityTypesViewType.__instance_acquisition_in_progress = False
        return ActivityTypesViewType.__instance

    ##########
    #   ViewType - Properties
    @property
    def mnemonic(self) -> str:
        return "ActivityTypes"

    @property
    def display_name(self) -> str:
        return GuiResources.string("ActivityTypesViewType.DisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return GuiResources.image("ActivityTypesViewType.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return GuiResources.image("ActivityTypesViewType.LargeImage")

    ##########
    #   Operations
    def create_view(self, parent: tk.BaseWidget) -> View:
        assert isinstance(parent, tk.BaseWidget)

        from .ActivityTypesView import ActivityTypesView
        return ActivityTypesView(parent)

##########
#   Register stock items
ViewType.register(ActivityTypesViewType.instance)
