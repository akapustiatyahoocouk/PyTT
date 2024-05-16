#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Activity import Activity
from .PrivateActivity import PrivateActivity
from .Task import Task
from ..resources.DbResources import DbResources

##########
#   Private entities
class PrivateTask(PrivateActivity, Task):
    """ A private task in a database. """

    ##########
    #   Constants
    TYPE_NAME = "PrivateTask"
    NAME_PROPERTY_NAME = PrivateActivity.NAME_PROPERTY_NAME
    DESCRIPTION_PROPERTY_NAME = PrivateActivity.DESCRIPTION_PROPERTY_NAME
    TIMEOUT_PROPERTY_NAME = PrivateActivity.TIMEOUT_PROPERTY_NAME
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = PrivateActivity.REQUIRE_COMMENT_ON_START_PROPERTY_NAME
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = PrivateActivity.REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME
    FULL_SCREEN_REMINDER_PROPERTY_NAME = PrivateActivity.FULL_SCREEN_REMINDER_PROPERTY_NAME
    ACTIVITY_TYPE_ASSOCIATION_NAME = PrivateActivity.ACTIVITY_TYPE_ASSOCIATION_NAME
    COMPLETED_PROPERTY_NAME = Task.COMPLETED_PROPERTY_NAME
    PARENT_ASSOCIATION_NAME = Task.PARENT_ASSOCIATION_NAME
    CHILDREN_ASSOCIATION_NAME = Task.CHILDREN_ASSOCIATION_NAME
    OWNER_ASSOCIATION_NAME = PrivateActivity.OWNER_ASSOCIATION_NAME

    ##########
    #   UI traits
    @property
    def type_name(self) -> str:
        return PrivateTask.TYPE_NAME

    @property
    def type_display_name(self) -> str:
        return DbResources.string("PrivateTask.TypeDisplayName")

    @property
    def small_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateTask.SmallImage")

    @property
    def large_image(self) -> tk.PhotoImage:
        return DbResources.image("PrivateTask.LargeImage")

