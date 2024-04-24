#   Python standard library
from typing import final, Set
from abc import abstractmethod, abstractproperty
import tkinter as tk

#   Internal dependencies on modules within the same component
from util.implementation.Annotations import staticproperty
from util.implementation.Metaclasses import ABCWithConstants
from util.implementation.Settings import Settings
from util.implementation.ComponentSettings import ComponentSettings
from util.implementation.Preference import Preference
from util.implementation.BoolPreference import BoolPreference

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
        assert isinstance(name, str) and name.isidentifier()

        self.__parent = parent
        self.__name = name
        self.__children = list()
        self.__preferences = list()
        
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
        return set(self.__children)

    @property
    def preferences(self) -> Set["Preference"]:
        return set(self.__preferences)

    ##########
    #   Operations
    def add_preference(self, preference: Preference) -> None:
        assert isinstance(preference, Preference)
        
        if preference not in self.__preferences:
            self.__preferences.append(preference)

    @staticmethod
    def load() -> None:
        section = Settings.get("Prefrences")
        for subroot in Preferences.ROOT.children:
            subroot.__load(section)

    @staticmethod
    def save() -> None:
        section = Settings.get("Prefrences")
        for subroot in Preferences.ROOT.children:
            subroot.__save(section)

    def create_editor(self, parent: tk.BaseWidget) -> tk.BaseWidget:
        """
            Creates a widget that acts as an interactive "editor"
            for this Preferences.
            
            @param parent:
                The parent widget for the new Preferences editor,
                cannot be None.
            @return:
                The newly created editor widget for this Preferences
                of None if this Preferences has nothing to edit.
        """
        assert isinstance(parent, tk.BaseWidget)
        return None
        
    ##########
    #   Implementation helpers
    def __load(self, section: ComponentSettings) -> None:
        #   Do the local preferences...
        for preference in self.__preferences:
            key = self.qualified_name + "." + preference.name
            try:
                if isinstance(preference, BoolPreference):
                    preference.value = section.get_bool(key, preference.value)
            except:
                pass    #   use default value of the Preference
        #   ...then the children
        for child in self.__children:
            child.__load(section)

    def __save(self, section: ComponentSettings) -> None:
        #   Do the local preferences...
        for preference in self.__preferences:
            key = self.qualified_name + "." + preference.name
            if preference.value is None:
                section.remove(key)
            else:
                try:
                    if isinstance(preference, BoolPreference):
                        section.put_bool(key, preference.value)
                except:
                    pass    #   use default value of the Preference
        #   ...then the children
        for child in self.__children:
            child.__save(section)
            