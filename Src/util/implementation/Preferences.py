#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import final, Set, Optional
from abc import abstractmethod, abstractproperty
import tkinter as tk

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Metaclasses import ABCWithConstants
from .Settings import Settings
from .ComponentSettings import ComponentSettings
from .Preference import Preference
from .BoolPreference import BoolPreference
from .LocalePreference import LocalePreference

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
    def ROOT() -> Preferences:
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
        self.__children = []
        self.__preferences = []
        
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
    def qualified_display_name(self) -> str:
        from .RootPreferences import RootPreferences
        if self.__parent is None:
            return ""
        elif isinstance(self.__parent, RootPreferences):
            return self.display_name
        else:
            return self.__parent.qualified_display_name + " / " + self.display_name

    @property
    def parent(self) -> Preferences:
        """ The immediate parent Preferences is this Preferences.
            The root Preferences of the Preferences tree has no
            parent, so this property there is None. """
        return self.__parent

    @property
    def children(self) -> Set["Preferences"]:
        return set(self.__children)

    @property
    def sort_order(self) -> Optional[int]:
        """ The relative sort order of this Preferences within
            ite immediate parent; None if sorted by display_name. """
        return None
    
    @property
    def preferences(self) -> Set["Preference"]:
        """ The set of all Preference settings under this Preferences. """
        return set(self.__preferences)

    ##########
    #   Operations
    def add_preference(self, preference: Preference) -> None:
        """
            Adds the specified Preference setting to this Preference.

            @param preference:
                The Preference setting to add to this Preferences.
        """
        assert isinstance(preference, Preference)
        
        if preference not in self.__preferences:
            self.__preferences.append(preference)

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

    def apply(self) -> None:
        """ Applies the current value of all Preference settings
            that exist under this Preferences to the currently
            running application. """
        pass            
        
    @staticmethod
    def load() -> None:
        """ Loads the entire Preferences tree from persistent Preferences.
            This means loaduing values of every Prefrence setting of
            every Prefrences node in the Prefrences tree. """
        section = Settings.get("Prefrences")
        for subroot in Preferences.ROOT.children:
            subroot.__load(section)

    @staticmethod
    def save() -> None:
        """ Saves the entire Preferences tree from persistent Preferences.
            This means saving values of every Prefrence setting of
            every Prefrences node in the Prefrences tree. """
        section = Settings.get("Prefrences")
        for subroot in Preferences.ROOT.children:
            subroot.__save(section)

    ##########
    #   Implementation helpers
    def __load(self, section: ComponentSettings) -> None:
        #   Do the local preferences...
        for preference in self.__preferences:
            key = self.qualified_name + "." + preference.name
            try:
                if isinstance(preference, BoolPreference):
                    preference.value = section.get_bool(key, preference.value)
                elif isinstance(preference, LocalePreference):
                    preference.value = section.get_locale(key, preference.value)
            except:
                pass    #   use default value of the Preference TODO and log ?
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
                    elif isinstance(preference, LocalePreference):
                        section.put_locale(key, preference.value)
                except:
                    pass    #   use default value of the Preference TODO and log ?
        #   ...then the children
        for child in self.__children:
            child.__save(section)
            