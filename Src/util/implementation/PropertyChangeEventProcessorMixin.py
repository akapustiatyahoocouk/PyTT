#   Python standard library
from typing import Callable, Union
from inspect import signature

#   Internal dependencies on modules within the same component
from .Event import Event
from .PropertyChangeEvent import PropertyChangeEvent
from .PropertyChangeEventListener import PropertyChangeEventListener
from .PropertyChangeEventHandler import PropertyChangeEventHandler

##########
#   Public entities
class PropertyChangeEventProcessorMixin:
    """ A mix-in class that can process property change events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        #   TODO make list elements WEAK references to actual listeners
        self.__property_change_listeners = list()
    
    ##########
    #   Operations
    def add_property_change_listener(self, l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Regsters the specified listener or handler to be 
            notified when a property change event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener 
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l not in self.__property_change_listeners:
            self.__property_change_listeners.append(l)

    def remove_property_change_listener(self, l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Un-regsters the specified listener or handler to no 
            longer be notified when a property change event is 
            processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener 
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l in self.__property_change_listeners:
            self.__property_change_listeners.remove(l)

    @property
    def property_change_listeners(self) -> list[Union[PropertyChangeEventListener, PropertyChangeEventHandler]]:
        """ The list of all property change listeners registered so far. """
        return self.__property_change_listeners.copy()

    def process_property_change_event(self, event : PropertyChangeEvent) -> bool:
        """ 
            Called to process an PropertyChangeEvent.
            
            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        for l in self.__property_change_listeners:
            try:
                if isinstance(l, PropertyChangeEventHandler):
                    l.on_property_change(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
