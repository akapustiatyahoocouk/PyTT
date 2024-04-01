#   Python standard library
from typing import Callable
from inspect import signature

from awt.Event import Event
from awt.KeyEvent import KeyEvent, KeyListener

class KeyEventProcessorMixin:
    """ A mix-in class that can process key events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        self.__key_listeners = list()
    
    ##########
    #   Event dispatch
    def add_key_listener(self, l: KeyListener) -> None:
        """ Regsters the specified listener to be notified when
            a key event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener 
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l not in self.__key_listeners:
            self.__key_listeners.append(l)

    def remove_key_listener(self, l: KeyListener) -> None:
        """ Un-regsters the specified listener to no longer be 
            notified when a key event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener 
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l in self.__key_listeners:
            self.__key_listeners.remove(l)

    @property
    def key_listeners(self) -> list[KeyListener]:
        """ The list of all key event listeners registered so far. """
        return self.__key_listeners.copy()

    ##########
    #   Operations (event processing) - normally, don't touch!
    def _process_key_event(self, event : KeyEvent) -> bool:
        """ 
            Called to process a KeyEvent.
            
            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The key event to process.
            @return:
                True if the event was processed, else false.
        """
        assert isinstance(event, KeyEvent)
        #   TODO if the event has NOY been processed, the default
        #   implementation should dispatch it to the "parent" event
        #   processor.
        for l in self.__key_listeners:
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
            @return:
                True if the event was processed, else false.
        """
        if isinstance(event, KeyEvent):
            process_key_event(self, event)
            return True
        else:
            return False
