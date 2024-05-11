#   Python standard library
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
#   Private entities
class PrivateActivity(Activity):
    """ A private activity in a database. """

    ##########
    #   Constants
    TYPE_NAME = "PrivateActivity"
    NAME_PROPERTY_NAME = Activity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = Activity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = Activity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = Activity.ACTIVITY_TYPE_ASSOCIATION_NAME
    OWNER_ASSOCIATION_NAME = "owner"

    ##########
    #   UI traits
    @property
    def type_name(self) -> str:
        return PrivateActivity.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("PrivateActivity.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateActivity.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateActivity.LargeImage")

    ##########
    #   Properties

    ##########
    #   Associations
    @abstractproperty
    def owner(self) -> "User":
        """
            The User to which this PrivateActivity belongs.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @owner.setter
    def owner(self, new_owner: "User") -> None:
        """
            Changes the User to which this PrivateActivity belongs.

            @param new_owner:
                The new User to which this PrivateActivity belongs.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
