#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Activity import Activity
from ..resources.DbResources import DbResources

##########
#   Public entities
class Task(Activity):
    """ A Task in a database. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = Activity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = Activity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = Activity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = Activity.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = "completed"
    PARENT_ASSOCIATION_NAME = "parent"
    CHILDREN_ASSOCIATION_NAME = "children"

    ##########
    #   Properties
    @abstractproperty
    def completed(self) -> bool:
        """
            True if this Task is completed, False if not.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @completed.setter
    def completed(self, new_completed: bool) -> None:
        """
            Specifies whether a Task is completed or not.

            @param new_completed:
                True if this Task is completed, False if not.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def parent(self) -> Optional[Task]:
        """
            The Immediate parent Task of this Task; None if none.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def children(self) -> Set[Task]:
        """
            The set of immediate children of this Task; can be empty but 
            cannot be None or contain Nones.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

