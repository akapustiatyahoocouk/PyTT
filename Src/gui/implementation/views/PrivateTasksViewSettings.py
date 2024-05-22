""" Persistent settings of the Admin skin. """
#   Python standard library
from typing import final, List, Optional

#   Dependencies on other PyTT components
from gui.interface.api import *
from util.interface.api import *

##########
#   Public entities
class PrivateTasksViewSettingsMeta(type):
    """ The metaclass for PrivateTasksViewSettings which implements
        gettable/settable static properties there. """

    ##########
    #   Construction
    def __init__(cls, *args, **kwargs):
        type.__init__(cls, *args, **kwargs)

        cls.__impl = Settings.get("PrivateTasksView")

    ##########
    #   Properties
    @property
    def hide_completed_tasks(cls) -> bool:
        """ True if the main frame is maximized, else False. """
        return cls.__impl.get_bool("hide_completed_tasks", False)

    @hide_completed_tasks.setter
    def hide_completed_tasks(cls, new_hide_completed_tasks: bool) -> None:
        """ Set to True if the main frame is maximized, else to False. """
        assert isinstance(new_hide_completed_tasks, bool)
        cls.__impl.put_bool("hide_completed_tasks", new_hide_completed_tasks)

@final
class PrivateTasksViewSettings(metaclass=PrivateTasksViewSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
