""" The "current" credentials. Placed in the gui component
    and not in the workspace component because the notion
    of the "current" Credentials is entirely a gui phenomenon. """

#   Python standard library
from typing import final, Optional

#   Dependencies on other PyTT components
from workspace.interface.api import *
from util.interface.api import *

##########
#   Public entities
@final
class CurrentCredentials:
    """ The "current" credentials. """

    ##########
    #   Constants (observable property names)
    CURRENT_CREDENTIALS_PROPERTY_NAME = "current"
    """ The name of the "current: Credentials" static property of a CurrentCredentials. """

    ##########
    #   Implementation
    __current_credentials = None
    __property_change_listeners = []

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

    ##########
    #   Operations    
    @staticmethod
    def get() -> Optional[Credentials]:
        """ The "current" Credentials, None if there isn't any. """
        return CurrentCredentials.__current_credentials

    @staticmethod
    def set(cc: Credentials) -> None:
        """ Sets the "current" Credentials, cannot be set to None. """
        assert isinstance(cc, Credentials)

        if cc is not CurrentCredentials.__current_credentials:
            CurrentCredentials.__current_credentials = cc
            #   Notify listeners of the "current" Workspace change
            evt = PropertyChangeEvent(CurrentCredentials, CurrentCredentials, CurrentCredentials.CURRENT_CREDENTIALS_PROPERTY_NAME)
            CurrentCredentials.process_property_change_event(evt)

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
        if l not in CurrentCredentials.__property_change_listeners:
            CurrentCredentials.__property_change_listeners.append(l)

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
        if l in CurrentCredentials.__property_change_listeners:
            CurrentCredentials.__property_change_listeners.remove(l)

    @staticproperty
    def property_change_listeners() -> list[Union[PropertyChangeEventListener, PropertyChangeEventHandler]]:
        """ The list of all static property change listeners registered so far. """
        return CurrentCredentials.__property_change_listeners.copy()

    @staticmethod
    def process_property_change_event(event : PropertyChangeEvent) -> bool:
        """
            Called to process an PropertyChangeEvent for a
            change made to a static property.

            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        for l in CurrentCredentials.property_change_listeners:
            try:
                if isinstance(l, PropertyChangeEventHandler):
                    l.on_property_change(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
