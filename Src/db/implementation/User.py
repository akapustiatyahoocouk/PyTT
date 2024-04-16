#   Python standard library
from abc import abstractproperty
import tkinter as tk

#   Dependencies on other PyTT components

#   Internal dependencies on modules within the same component
from db.implementation.DatabaseObject import DatabaseObject

##########
#   Public entities
class User(DatabaseObject):
    """ A User in a database. """

    ##########
    #   UI traits
    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this database object. """
        raise NotImplementedError()

    @abstractproperty
    def type_name(self) -> str:
        """ The internal name of this database object's type (e.g. "User",
            "PublicTask", etc.) """
        raise NotImplementedError()

    @abstractproperty
    def type_display_name(self) -> str:
        """ The user-readable display name of this database object's type
            (e.g. "user", "public task", etc.) """
        raise NotImplementedError()

    @abstractproperty
    def small_image(self) -> tk.PhotoImage:
        """ The small (16x16) image representing this datbase object. """
        raise NotImplementedError()

    @abstractproperty
    def large_image(self) -> tk.PhotoImage:
        """ The large (32x32) image representing this datbase object. """
        raise NotImplementedError()

    ##########
    #   Properties

    ##########
    #   Operations
        