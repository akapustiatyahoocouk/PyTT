""" Defines a Localizable Subsystem ADT. """
#   Python standard library
from typing import Optional, Set
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .Locale import Locale
from .Subsystem import Subsystem

##########
#   Public entities
class LocalizableSubsystem(Subsystem):
    """ A "subsystem" that provides localization facilities. """

    ##########
    #   Construction
    def __init__(self, parent: Optional[Subsystem]):
        Subsystem.__init__(self, parent)

    ##########
    #   Properties
    @abstractproperty
    def supported_locales(self) -> set[Locale]:
        """ The set of all locales supported by this Subsystem. """
        raise NotImplementedError()

    ##########
    #   Properties - subsystem registry access
    @staticmethod
    def all_supported_locales() -> Set[Locale]:
        result = set()
        LocalizableSubsystem.__collect_supported_locales(result, Subsystem.ROOT)
        return result

    ##########
    #   Implementation
    @staticmethod
    def __collect_supported_locales(locales: Set[Locale], subsystem: Subsystem) -> None:
        if isinstance(subsystem, LocalizableSubsystem):
            locales.update(subsystem.supported_locales)
        for child in subsystem.children:
            LocalizableSubsystem.__collect_supported_locales(locales, child)
