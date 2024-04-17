#   Python standard library
from typing import Callable, Union
from inspect import signature

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .KeyEvent import KeyEvent
from .KeyEventListener import KeyEventListener
from .KeyEventHandler import KeyEventHandler

##########
#   Public entities
class KeyEventProcessorMixin:
    """ A mix-in class that can process key events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        #   TODO make list elements WEAK references to actual listeners
        self.__key_listeners = list()

    ##########
    #   Operations
    def add_key_listener(self, l: Union[KeyEventListener, KeyEventHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when a key event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, KeyEventHandler))
        if l not in self.__key_listeners:
            self.__key_listeners.append(l)

    def remove_key_listener(self, l: Union[KeyEventListener, KeyEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a key event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, KeyEventHandler))
        if l in self.__key_listeners:
            self.__key_listeners.remove(l)

    @property
    def key_listeners(self) -> list[Union[KeyEventListener, KeyEventHandler]]:
        """ The list of all key event listeners registered so far. """
        return self.__key_listeners.copy()

    def process_key_event(self, event : KeyEvent) -> bool:
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
        for l in self.key_listeners:
            try:
                if isinstance(l, KeyEventHandler):
                    match event.event_type:
                        case KeyEventType.KEY_DOWN:
                            l.on_key_down(event)
                        case KeyEventType.KEY_UN:
                            l.on_key_up(event)
                        case KeyEventType.KEY_CHAR:
                            l.on_key_char(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
