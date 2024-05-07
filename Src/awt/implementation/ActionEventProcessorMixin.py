""" Defines a mix-in for Action event processing capability. """
#   Python standard library
from typing import Callable, Union
from inspect import signature
import traceback

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent
from .ActionEventListener import ActionEventListener
from .ActionEventHandler import ActionEventHandler

##########
#   Public entities
class ActionEventProcessorMixin:
    """ A mix-in class that can process action events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        #   TODO make list elements WEAK references to actual listeners
        self.__action_listeners = []

    ##########
    #   Operations
    def add_action_listener(self, l: Union[ActionEventListener, ActionEventHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when an action event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, ActionEventHandler))
        if l not in self.__action_listeners:
            self.__action_listeners.append(l)

    def remove_action_listener(self, l: Union[ActionEventListener, ActionEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when an action event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, ActionEventHandler))
        if l in self.__action_listeners:
            self.__action_listeners.remove(l)

    @property
    def action_listeners(self) -> list[Union[ActionEventListener, ActionEventHandler]]:
        """ The list of all action event listeners registered so far. """
        return self.__action_listeners.copy()

    def process_action_event(self, event : ActionEvent) -> bool:
        """
            Called to process an ActionEvent.

            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The action event to process.
        """
        assert isinstance(event, ActionEvent)
        for l in self.action_listeners:
            try:
                if isinstance(l, ActionEventHandler):
                    l.on_action(event)
                else:
                    l(event)
            except Exception:
                #   TODO log the exception
                print(traceback.format_exc())
        return event.processed
