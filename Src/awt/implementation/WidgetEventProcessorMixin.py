#   Python standard library
from typing import Callable, Union
from inspect import signature
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .WidgetEvent import WidgetEvent
from .WidgetEventListener import WidgetEventListener
from .WidgetEventHandler import WidgetEventHandler
from .WidgetEventType import WidgetEventType

##########
#   Public entities
class WidgetEventProcessorMixin:
    """ A mix-in class that can process widget events. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        #   TODO make list elements WEAK references to actual listeners
        self.__widget_listeners = list()

    ######
    #   Operations
    def add_widget_listener(self, l: Union[WidgetEventListener, WidgetEventHandler]) -> None:
        """ Regsters the specified listener or handler to be
            notified when a widget event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WidgetEventHandler))
        if l not in self.__widget_listeners:
            self.__widget_listeners.append(l)

    def remove_widget_listener(self, l: Union[WidgetEventListener, WidgetEventHandler]) -> None:
        """ Un-regsters the specified listener or handler to no
            longer be notified when a widget event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WidgetEventHandler))
        if l in self.__widget_listeners:
            self.__widget_listeners.remove(l)

    @property
    def widget_listeners(self) -> list[Union[WidgetEventListener, WidgetEventHandler]]:
        """ The list of all widget event listeners and handlers
            registered so far. """
        return self.__widget_listeners.copy()

    def process_widget_event(self, event : WidgetEvent) -> bool:
        """
            Called to process a WidgetEvent.

            @param self:
                The EventProcessor on which the method has been called.
            @param event:
                The widget event to process.
            @return:
                True if the event was processed, else false.
        """
        assert isinstance(event, WidgetEvent)
        for l in self.__widget_listeners:
            try:
                if isinstance(l, WidgetEventHandler):
                    match event.event_type:
                        case WidgetEventType.WIDGET_SHOWN:
                            l.on_widget_shown(event)
                        case WidgetEventType.WIDGET_HIDDEN:
                            l.on_widget_hidden(event)
                        case WidgetEventType.WIDGET_MOVED:
                            l.on_widget_moved(event)
                        case WidgetEventType.WIDGET_RESIZED:
                            l.on_widget_resized(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
