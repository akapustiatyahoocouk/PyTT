""" The "current" workspace. Placed in the gui component
    and not in the workspace component because the notion
    of the "current" Workspace is entirely a gui phenomenon. """

#   Python standard library
from typing import final, Optional

#   Dependencies on other PyTT components
from workspace.interface.api import *
from util.interface.api import *

##########
#   Public entities
@final
class CurrentWorkspace(ClassWithConstants):
    """ The "current" Workspace. """

    ##########
    #   Constants (observable property names)
    CURRENT_WORKSPACE_PROPERTY_NAME = "current"
    """ The name of the "current: Workspace" static property of a CurrentWorkspace. """

    ##########
    #   Implementation
    __current_workspace = None
    __property_change_listeners = []

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

    ##########
    #   Operations    
    @staticmethod
    def get() -> Optional[Workspace]:
        """ The "current" Workspace, None if there isn't any. """
        return CurrentWorkspace.__current_workspace

    @staticmethod
    def set(cc: Workspace) -> None:
        """ Sets the "current" Workspace, None to make sure there isn't any. """
        assert (cc is None) or isinstance(cc, Workspace)

        if cc is not CurrentWorkspace.__current_workspace:
            CurrentWorkspace.__current_workspace = cc
            #   Notify listeners of the "current" Workspace change
            evt = PropertyChangeEvent(CurrentWorkspace, CurrentWorkspace, CurrentWorkspace.CURRENT_WORKSPACE_PROPERTY_NAME)
            CurrentWorkspace.process_property_change_event(evt)

    ##########
    #   Operations (static property change handling)
    @staticmethod
    def add_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when a static property change event is
            processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l not in CurrentWorkspace.__property_change_listeners:
            CurrentWorkspace.__property_change_listeners.append(l)

    @staticmethod
    def remove_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a static property change
            event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l in CurrentWorkspace.__property_change_listeners:
            CurrentWorkspace.__property_change_listeners.remove(l)

    @staticproperty
    def property_change_listeners() -> list[Union[PropertyChangeEventListener, PropertyChangeEventHandler]]:
        """ The list of all static property change listeners registered so far. """
        return CurrentWorkspace.__property_change_listeners.copy()

    @staticmethod
    def process_property_change_event(event : PropertyChangeEvent) -> bool:
        """
            Called to process an PropertyChangeEvent for a
            change made to a static property.

            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        for l in CurrentWorkspace.property_change_listeners:
            try:
                if isinstance(l, PropertyChangeEventHandler):
                    l.on_property_change(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
