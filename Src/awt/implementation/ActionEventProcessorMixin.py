"""
    Defines a mix-in for Action event processing capability.
"""
#   Python standard library
from typing import Callable
from inspect import signature

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from awt.implementation.ActionEvent import ActionEvent, ActionListener

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
        self.__action_listeners = []

    ##########
    #   Operations
    def add_action_listener(self, l: ActionListener) -> None:
        """ Regsters the specified listener to be notified when
            an action event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l not in self.__action_listeners:
            self.__action_listeners.append(l)

    def remove_action_listener(self, l: ActionListener) -> None:
        """ Un-regsters the specified listener to no longer be
            notified when an action event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert isinstance(l, Callable) and len(signature(l).parameters) == 1
        if l in self.__action_listeners:
            self.__action_listeners.remove(l)

    @property
    def action_listeners(self) -> list[ActionListener]:
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
        #   TODO if the event has NOY been processed, the default
        #   implementation should dispatch it to the "parent" event
        #   processor.
        for l in self.__action_listeners:
            l(event)    #   TODO catch & log exception, then go to the next listener
        return True
