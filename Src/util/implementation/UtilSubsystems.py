""" Subsysems defined by the Util compnent. """

#   Python standard library
from typing import Optional, Set, final
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Subsystem import Subsystem
from .LocalizableSubsystem import LocalizableSubsystem
from .Locale import Locale
from ..resources.UtilResources import UtilResources

##########
#   Public entities
@final
class RootSubsystem(LocalizableSubsystem):
    """ The root "/" of the subsustems tree. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert RootSubsystem.__instance_acquisition_in_progress, "Use RootSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, None)

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
    
@final
class UtilitiesSubsystem(LocalizableSubsystem):
    """ The "/Utilities" Subsystem, actins as a parent
        for concrete subsystems falling into this category. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert UtilitiesSubsystem.__instance_acquisition_in_progress, "Use UtilitiesSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, RootSubsystem.instance)

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

@final
class UiSubsystem(LocalizableSubsystem):
    """ The "/Ui" Subsystem, actins as a parent
        for concrete subsystems falling into this category. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert UiSubsystem.__instance_acquisition_in_progress, "Use UiSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, RootSubsystem.instance)

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

@final
class StorageSubsystem(LocalizableSubsystem):
    """ The "/Storage" Subsystem, actins as a parent
        for concrete subsystems falling into this category. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert StorageSubsystem.__instance_acquisition_in_progress, "Use StorageSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, RootSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if StorageSubsystem.__instance is None:
            StorageSubsystem.__instance_acquisition_in_progress = True
            StorageSubsystem.__instance = StorageSubsystem()
            StorageSubsystem.__instance_acquisition_in_progress = False
        return StorageSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        return UtilResources.string("StorageSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        return UtilResources.factory.supported_locales

##########
#   Instantiate
RootSubsystem.instance
UtilitiesSubsystem.instance
UiSubsystem.instance
StorageSubsystem.instance
