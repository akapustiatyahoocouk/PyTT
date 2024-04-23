#   Python standard library
from typing import final, Set
from abc import abstractproperty

#   Internal dependencies on modules within the same component
from util.implementation.Metaclasses import ABCWithConstants
from util.implementation.Settings import Settings
from util.implementation.ComponentSettings import ComponentSettings
from util.implementation.Annotations import staticproperty

##########
#   Public entities
class Preferences(ABCWithConstants):
    """
        A bunch of relater persistent preference items
        that are made persistent in the Settings.

        Concrete preferences will normally be singletons
        registered by plugins.
        
        All Preferences are organized into a tree, with 
        the artificial "root preferences" node at the root 
        of that tree. The "root preferences" node itself
        does not carry any preference items, so there's
        nothing to persist for that node. 
    """

    ##########
    #   Constants
    @staticproperty
    def ROOT() -> "Preferences":
        """ The root of the Preferences tree. """
        from .RootPreferences import RootPreferences
        return RootPreferences.instance
    
    ##########
    #   Construction - from derived classes only.
    def __init__(self, parent: "Preferences", name: str) -> None:
        assert (parent is None) or isinstance(parent, Preferences)
        assert isinstance(name, str)

        self.__parent = parent
        self.__name = name
        self.__children = list()

        if parent is not None:
            parent.__children.append(self)

    ##########
    #   Properties
    @property
    def name(self) -> str:
        """ The own name of this Preferences. """
        return self.__name

    @property
    def qualified_name(self) -> str:
        """ The qualified name of this Preferences consists of
            the names of all parent Preferences from the root of 
            the Preferences tree to this Preferences node,
            separated by "/". """
        if self.__parent is None:
            return ""
        else:
            return self.__parent.qualified_name + "/" + self.__name

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this Preferences. """
        raise NotImplementedError()

    @property
    def parent(self) -> "Preferences":
        """ The immediate parent Preferences is this Preferences.
            The root Preferences of the Preferences tree has no
            parent, so this property there is None. """
        return self.__parent

    @property
    def children(self) -> Set["Preferences"]:
        return set(parent.__children)

    ##########
    #   Operations
    @staticmethod
    def load() -> None:
        section = Settings.get("Prefrences")
        pass

    @staticmethod
    def save() -> None:
        section = Settings.get("Prefrences")
        pass
