#   Python standard library
from typing import Optional, List, Set
from abc import abstractproperty
import tkinter as tk
from .Capabilities import Capabilities

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseObject import DatabaseObject
from ..resources.DbResources import DbResources

##########
#   Public entities
class Activity(DatabaseObject):
    """ An Activity in a database. """

    ##########
    #   Constants
    NAME_PROPERTY_NAME = "name"
    DESCRIPTION_PROPERTY_NAME = "description"
    TIMEOUT_PROPERTY_NAME = "timeout"
    REQUIRE_COMMENT_ON_START_PROPERTY_NAME = "requireCommentOnStart"
    REQUIRE_COMMENT_ON_FINISH_PROPERTY_NAME = "requireCommentOnFinish"
    FULL_SCREEN_REMINDER_PROPERTY_NAME = "fullScreenReminder"
    ACTIVITY_TYPE_ASSOCIATION_NAME = "activityTYpe"

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

    @abstractproperty
    def timeout(self) -> Optional[int]:
        """
            The timeout of this Activity, expressed in minutes, or
            None if this Activity has no timeout.

            When an Activity has the "timeout" configured, then when a
            user starts that Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @timeout.setter
    def timeout(self, new_timeout: Optional[int]) -> None:
        """
            Sets the "timeout" of this Activity.

            When an Activity has the "timeout" configured, then when a
            user starts that Activity and does nothing at all for
            that period of time, the Activity ends automatically.

            @param new_timeout:
                The new "timeout" for this Activity, expressed in minutes,
                or None to remove the timeout from this Activity.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def require_comment_on_start(self) -> bool:
        """
            True if a user is required to make a comment when starting
            this Activity, False if not. These comments are recorded as
            Events in the database.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @require_comment_on_start.setter
    def require_comment_on_start(self, new_require_comment_on_start: bool) -> None:
        """
            Specifies whether a user is required to make a comment when
            starting this Activity. These comments are recorded as Events
            in the database.

            @param new_require_comment_on_start:
                True to mark this Activity as requiring a comment whan a
                user starts it, False to make this Activity not require
                a user comment when starting it.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def require_comment_on_finish(self) -> bool:
        """
            True if a user is required to make a comment when finishing
            this Activity, False if not. These comments are recorded as
            Events in the database.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @require_comment_on_finish.setter
    def require_comment_on_finish(self, new_require_comment_on_finish: bool) -> None:
        """
            Specifies whether a user is required to make a comment when
            finishing this Activity. These comments are recorded as Events
            in the database.

            @param new_require_comment_on_finish:
                True to mark this Activity as requiring a comment whan a
                user finishes it, False to make this Activity not require
                a user comment when finishing it.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractproperty
    def full_screen_reminder(self) -> bool:
        """
            True if a user shall see a full-screen reminder when this Activity 
            is underway (useful for activities such as "in a meeting", "on a 
            lunch break", etc.), so that the user is reminded to "end" the 
            Activity when starting on something else.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @full_screen_reminder.setter
    def full_screen_reminder(self, new_full_screen_reminder: bool) -> None:
        """
            True if a user shall see a full-screen reminder when this Activity 
            is underway (useful for activities such as "in a meeting", "on a 
            lunch break", etc.), so that the user is reminded to "end" the 
            Activity when starting on something else.

            @param new_full_screen_reminder:
                True to mark this Activity as providing a full-screen reminder
                to the user when the Activity is underway, False to not privide
                such full-screen reminder when the Activity is underway.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Associations
    @abstractproperty
    def activity_type(self) -> Optional["ActivityType"]:
        """
            The ActivityType assigned to this Activity, None if this 
            Activity is not assigned an ActivityType.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @activity_type.setter
    def activity_type(self, new_activity_type: Optional["ActivityType"]) -> None:
        """
            Assigns the specified ActivityType to this Activity.

            @param new_activity_type:
                The ActivityType to assign to this Activity, None == none.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
