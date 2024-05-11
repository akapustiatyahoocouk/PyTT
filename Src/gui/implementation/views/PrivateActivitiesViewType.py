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
class PrivateActivitiesViewType(ViewType):

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : ViewType = None

    def __init__(self):
        assert PrivateActivitiesViewType.__instance_acquisition_in_progress, "Use PrivateActivitiesViewType.instance() instead"
        ViewType.__init__(self)

    @staticproperty
    def instance() -> ViewType:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if PrivateActivitiesViewType.__instance is None:
            PrivateActivitiesViewType.__instance_acquisition_in_progress = True
            PrivateActivitiesViewType.__instance = PrivateActivitiesViewType()
            PrivateActivitiesViewType.__instance_acquisition_in_progress = False
        return PrivateActivitiesViewType.__instance

    ##########
    #   ViewType - Properties
    @property
    def mnemonic(self) -> str:
        return "PrivateActivities"

    @property
    def display_name(self) -> str:
        return GuiResources.string("PrivateActivitiesViewType.DisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return GuiResources.image("PrivateActivitiesViewType.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return GuiResources.image("PrivateActivitiesViewType.LargeImage")

    ##########
    #   Operations
    def create_view(self, parent: tk.BaseWidget) -> View:
        assert isinstance(parent, tk.BaseWidget)

        from .PrivateActivitiesView import PrivateActivitiesView
        return PrivateActivitiesView(parent)

##########
#   Register stock items
ViewType.register(PrivateActivitiesViewType.instance)


