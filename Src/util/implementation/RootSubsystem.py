""" Defines a root "/" of the Subsystems tree. """
#   Python standard library
from typing import Optional, Set
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Subsystem import Subsystem
from .LocalizableSubsystem import LocalizableSubsystem
from .Locale import Locale
from ..resources.UtilResources import UtilResources

##########
#   Public entities
class RootSubsystem(LocalizableSubsystem):
    """ The root "/" of the subsustems tree. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert RootSubsystem.__instance_acquisition_in_progress, "Use RootSubsystem.instance instead"
        Subsystem.__init__(self, None)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if RootSubsystem.__instance is None:
            RootSubsystem.__instance_acquisition_in_progress = True
            RootSubsystem.__instance = RootSubsystem()
            RootSubsystem.__instance_acquisition_in_progress = False
        return RootSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        return UtilResources.string("RootSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        return UtilResources.factory.supported_locales
    
##########
#   Instantiate
RootSubsystem.instance
