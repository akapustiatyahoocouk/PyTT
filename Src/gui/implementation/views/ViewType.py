#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional
from abc import ABC, abstractmethod, abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
class ViewType(ABC):

    ##########
    #   Properties
    @abstractproperty
    def mnemonic(self) -> str:
        """ The mnemonic identifier of this view type. """
        raise NotImplementedError()

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this view type
            for the current default locale. """
        raise NotImplementedError()

    @abstractproperty
    def small_image(self) -> tk.PhotoImage:
        """ The small (16x16) image representing views of this type. """
        raise NotImplementedError()

    @abstractproperty
    def large_image(self) -> tk.PhotoImage:
        """ The large (32x32) image representing views of this type. """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def create_view(self, parent: tk.BaseWidget) -> View:
        """
            Creates a new View of this type.

            @param parent:
                The paret widget for the new View.
            @return:
                The newly created View.
        """
        raise NotImplementedError()

    ##########
    #   Registry
    __registry : dict[str, "ViewType"] = {}

    @staticmethod
    def register(view_type: "ViewType") -> bool:
        """ "Registers" the specified view type.
            Returns True on  success, False on failure. """
        assert isinstance(view_type, ViewType)

        print('Registering', view_type.display_name, 'view type [' +
              view_type.mnemonic + ']')
        if view_type.mnemonic in ViewType.__registry:
            return ViewType.__registry[view_type.mnemonic] is view_type
        else:
            ViewType.__registry[view_type.mnemonic] = view_type
            return True

    @staticmethod
    def find(mnemonic: str) -> Optional[ViewType]:
        """ Finds a registered view type by mnemonic;
            returns None if not found. """
        return ViewType.__registry.get(mnemonic, None)

    @staticproperty
    def all() -> set[ViewType]:
        """ The 'set' of all registered view types. """
        return set(ViewType.__registry.values())
