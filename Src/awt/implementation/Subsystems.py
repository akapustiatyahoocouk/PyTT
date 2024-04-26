""" Defines the AWT subsystem. """
#   Python standard library
from typing import Optional, Set
from abc import ABC, abstractproperty

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from ..resources.AwtResources import AwtResources

##########
#   Public entities
class AwtSubsystem(LocalizableSubsystem):
    """ The root "Ui/AWT" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert AwtSubsystem.__instance_acquisition_in_progress, "Use AwtSubsystem.instance instead"
        Subsystem.__init__(self, UiSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if AwtSubsystem.__instance is None:
            AwtSubsystem.__instance_acquisition_in_progress = True
            AwtSubsystem.__instance = AwtSubsystem()
            AwtSubsystem.__instance_acquisition_in_progress = False
        return AwtSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        return AwtResources.string("AwtSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        return AwtResources.factory.supported_locales

##########
#   Instantiate
AwtSubsystem.instance
