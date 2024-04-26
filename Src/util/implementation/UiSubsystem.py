""" Defines the "/Ui" Subsystem. """
#   Python standard library
from typing import Optional, Set
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Subsystem import Subsystem
from .LocalizableSubsystem import LocalizableSubsystem
from .RootSubsystem import RootSubsystem
from .Locale import Locale
from ..resources.UtilResources import UtilResources

##########
#   Public entities
class UiSubsystem(LocalizableSubsystem):
    """ The "/Ui" Subsystem, actins as a parent
        for concrete subsystems falling into this category. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert UiSubsystem.__instance_acquisition_in_progress, "Use UiSubsystem.instance instead"
        Subsystem.__init__(self, RootSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if UiSubsystem.__instance is None:
            UiSubsystem.__instance_acquisition_in_progress = True
            UiSubsystem.__instance = UiSubsystem()
            UiSubsystem.__instance_acquisition_in_progress = False
        return UiSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        return UtilResources.string("UiSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        return UtilResources.factory.supported_locales

##########
#   Instantiate
UiSubsystem.instance
