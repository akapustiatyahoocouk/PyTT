from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

import awt_impl.BaseWidgetMixin
import awt_impl.ActionEvent
import awt_impl.KeyEventProcessorMixin
import awt_impl.ActionEventProcessorMixin

class Button(ttk.Button, 
             awt_impl.BaseWidgetMixin.BaseWidgetMixin,
             awt_impl.KeyEventProcessorMixin.KeyEventProcessorMixin,
             awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin):
    """ A ttk.Button with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Button widget with the parent master. """
        ttk.Button.__init__(self, master, **kwargs)
        awt_impl.KeyEventProcessorMixin.KeyEventProcessorMixin.__init__(self)
        awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin.__init__(self)

        self.__action_event_listeners = list()
        self.configure(command = self.__on_tk_click)

    ##########
    #   Operations (event processing) - normally, don't touch!
    def _process_event(self, event : awt_impl.Event.Event):
        return (awt_impl.KeyEventProcessorMixin.KeyEventProcessorMixin._process_event(self, event) or
                awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin._process_event(self, event))

    ##########
    #   Event listeners
    def __on_tk_click(self):
        self._process_action_event(awt_impl.ActionEvent.ActionEvent(self))
