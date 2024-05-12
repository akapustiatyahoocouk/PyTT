""" Defines a Subsystem ADT. """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, Set
from abc import ABC, abstractproperty

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Metaclasses import ABCWithConstants

##########
#   Public entities
class Subsystem(ABCWithConstants):
    """ A "subsystem" is a PyTT component that is responsible
        for a certain aspect of PyTT functionality. All subsystems
        are organised into a tree with an artificial "PyTT" root
        subsystem as the root of that tree. """

    ##########
    #   Constants
    @staticproperty
    def ROOT() -> Subsystem:
        """ The root of the Subsystems tree. """
        from .UtilSubsystems import RootSubsystem
        return RootSubsystem.instance

    ##########
    #   Construction
    def __init__(self, parent: Optional["Subsystem"]):
        assert (parent is None) or isinstance(parent, Subsystem)

        self.__parent = parent
        self.__children = []
        if parent is not None:
            parent.__children.append(self)

    ##########
    #   Properties
    @property
    def parent(self) -> Optional["Subsystem"]:
        """ The immediate parent Subsystem of this Subsystem, or
            None if this is a root Subsystem. """
        return self.__parent

    @property
    def children(self) -> Set["Subsystem"]:
        """ An unordered set of all immediate children of this
            Subsystem. """
        return set(self.__children)

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this subsystem for
        the current default locale. """
        raise NotImplementedError()

    @property
    def qualified_display_name(self) -> str:
        """ The fully qualified user-readable display name of this
            Subsystem for the current default locale, from the root 
            to this Subsystem, that uses "/" as a name component 
            separator. """
        if self.parent is None:
            return self.display_name
        else:
            return self.parent.qualified_display_name + " / " + self.display_name
