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
#   Public entities
class PublicActivity(Activity):
    """ A public activity in a database. """

    ##########
    #   Constants
    TYPE_NAME = "PublicActivity"
    NAME_PROPERTY_NAME = Activity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = Activity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = Activity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = Activity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = Activity.FULL_SCREEN_REMINDER_PROPERTY_NAME

    ##########
    #   UI traits
    @property
    def type_name(self) -> str:
        return PublicActivity.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("PublicActivity.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("PublicActivity.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("PublicActivity.LargeImage")

    ##########
    #   Properties

    ##########
    #   Associations
