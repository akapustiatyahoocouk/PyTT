""" A common base class for all objects residing in a database. """

#   Python standard library
from typing import TypeAlias
from abc import ABC, abstractproperty, abstractmethod
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from db.implementation.Database import Database

##########
#   Public entities
OID: TypeAlias = int

class DatabaseObject(ABCWithConstants):
    """ A common base class for all objects residing in a database. """

    ##########
    #   object
    def __str__(self) -> str:
        return self.type_display_name + ' ' + self.display_name

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
    @abstractproperty
    def database(self) -> Database:
        """ The database to which this object belongs if live) or used
            to belong (if dead). """
        raise NotImplementedError()

    @abstractproperty
    def live(self) -> bool:
        """ True of this satabase object [proxy] is live, false if dead. """
        raise NotImplementedError()

    @abstractproperty
    def oid(self) -> OID:
        """ The OID of this object (if live) or the OID this object
            used to have (if dead). """
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    @abstractmethod
    def destroy(self) -> None:
        """
            Destroys this object, delete-cascading as necessary.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
