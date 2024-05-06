#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseObject import DatabaseObject
from .Activity import Activity
from ..resources.DbResources import DbResources

##########
#   Public entities
class Activity(DatabaseObject):
    """ An Activity type in a database. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = "name"
    DESCRIPTION_PROPERTY_NAME = "description"

    ##########
    #   UI traits
    @property
    def display_name(self) -> str:
        try:
            return self.name
        except Exception as ex:
            return str(ex)

    ##########
    #   Properties
    @abstractproperty
    def name(self) -> str:
        """
            The "name" of this ActivityType.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @name.setter
    def name(self, new_name: str) -> None:
        """
            Sets the "name" of this ActivityType.

            @param new_name:
                The new "name" for this ActivityType.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def description(self) -> str:
        """
            The "description" of this ActivityType (multiline, "\n" - separated).

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @description.setter
    def description(self, new_description: str) -> None:
        """
            Sets the "description" of this ActivityType.

            @param new_description:
                The new "description" for this ActivityType (multiline, "\n" - separated).
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def activities(self) -> Set[Activity]:
        """
            The set of all Activities assigned this ActivityType.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
