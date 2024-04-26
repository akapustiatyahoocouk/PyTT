""" Defines the "/Utilities" Subsystem. """
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
class UtilitiesSubsystem(LocalizableSubsystem):
    """ The "/Utilities" Subsystem, actins as a parent
        for concrete subsystems falling into this category. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert UtilitiesSubsystem.__instance_acquisition_in_progress, "Use UtilitiesSubsystem.instance instead"
        Subsystem.__init__(self, RootSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if UtilitiesSubsystem.__instance is None:
            UtilitiesSubsystem.__instance_acquisition_in_progress = True
            UtilitiesSubsystem.__instance = UtilitiesSubsystem()
            UtilitiesSubsystem.__instance_acquisition_in_progress = False
        return UtilitiesSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        return UtilResources.string("UtilitiesSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        return UtilResources.factory.supported_locales

##########
#   Instantiate
UtilitiesSubsystem.instance
