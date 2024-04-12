#   Python standard library
from typing import Callable, Union
from inspect import signature

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent
from .ItemEventListener import ItemEventListener
from .ItemEventHandler import ItemEventHandler

##########
#   Public entities
class ItemEventProcessorMixin:
    """ A mix-in class that can process item events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        #   TODO make list elements WEAK references to actual listeners
        self.__item_listeners = list()
    
    ##########
    #   Operations
    def add_item_listener(self, l: Union[ItemEventListener, ItemEventHandler]) -> None:
        """ Registers the specified listener or handler to be 
            notified when an item event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener 
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, ItemEventHandler))
        if l not in self.__item_listeners:
            self.__item_listeners.append(l)

    def remove_item_listener(self, l: Union[ItemEventListener, ItemEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no 
            longer be notified when an item event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener 
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, ItemEventHandler))
        if l in self.__item_listeners:
            self.__item_listeners.remove(l)

    @property
    def item_listeners(self) -> list[Union[ItemEventListener, ItemEventHandler]]:
        """ The list of all item event listeners registered so far. """
        return self.__item_listeners.copy()

    def process_item_event(self, event : ItemEvent) -> bool:
        """ 
            Called to process an ItemEvent.
            
            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The item event to process.
            @return:
                True if the event was processed, else false.
        """
        assert isinstance(event, ItemEvent)
        for l in self.item_listeners:
            try:
                if isinstance(l, ItemEventHandler):
                    match event.event_type:
                        case ItemEventType.ITEM_SELECTED:
                            l.on_item_selected(event)
                        case ItemEventType.ITEM_UNSELECTED:
                            l.on_item_unselected(event)
                        case ItemEventType.ITEM_STATE_CHANGED:
                            l.on_item_state_changed(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
