from typing import Callable
from inspect import signature

from awt.Event import Event
from awt.PropertyChangeEvent import PropertyChangeEvent, PropertyChangeListener

class PropertyChangeEventProcessorMixin:
    """ A mix-in class that can process property change events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        self.__property_change_listeners = list()
    
    ##########
    #   Event dispatch
    def add_property_change_listener(self, l: PropertyChangeListener) -> None:
        """ Regsters the specified listener to be notified when
            a property change event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener 
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l not in self.__property_change_listeners:
            self.__property_change_listeners.append(l)

    def remove_property_change_listener(self, l: PropertyChangeListener) -> None:
        """ Un-regsters the specified listener to no longer be 
            notified when a property change event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener 
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l in self.__property_change_listeners:
            self.__property_change_listeners.remove(l)

    @property
    def property_change_listeners(self) -> list[PropertyChangeListener]:
        """ The list of all property change listeners registered so far. """
        return self.__property_change_listeners.copy()

    ##########
    #   Operations (event processing) - normally, don't touch!
    def _process_property_change_event(self, event : PropertyChangeEvent) -> bool:
        """ 
            Called to process an PropertyChangeEvent.
            
            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        #   TODO if the event has NOY been processed, the default
        #   implementation should dispatch it to the "parent" event
        #   processor.
        for l in self.__property_change_listeners:
            l(event)    #   TODO catch & log exception, then go to the next listener
        return True
    
    def _process_event(self, event : Event) -> bool:
        """ 
            Called to process a generic Event.
            Default implementation analyses the event type and then
            dispatches the event to the appropriate process_XXX_event()
            method, where XXX depends on the event type.
            
            TODO to speed thing up, use a map of event classes to event
                 handler methods ?
            
            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The event to process.
        """
        if isinstance(event, PropertyChangeEvent):
            process_property_change_event(self, event)
            return True
        else:
            return False


