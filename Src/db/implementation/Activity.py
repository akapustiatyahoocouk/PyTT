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
    """ An Activity in a database. """

    ##########
    #   Constants
    TYPE_NAME = "Activity"
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

    @property
    def type_name(self) -> str:
        return Activity.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("Activity.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("Activity.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("Activity.LargeImage")

    ##########
    #   Properties
    @abstractproperty
    def name(self) -> str:
        """
            The "name" of this Activity.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @name.setter
    def name(self, new_name: str) -> None:
        """
            Sets the "name" of this Activity.

            @param new_name:
                The new "name" for this Activity.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def description(self) -> str:
        """
            The "description" of this Activity (multiline, "\n" - separated).

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @description.setter
    def description(self, new_description: str) -> None:
        """
            Sets the "description" of this Activity.

            @param new_description:
                The new "description" for this Activity (multiline, "\n" - separated).
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def activity_type(self) -> Optional["ActivityType"]:
        """
            The ActivityType assigned to this Activity,
                None if this Activity is not assigned an ActivityType.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
