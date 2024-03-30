from typing import Callable
from inspect import signature

import tkinter as tk
import tkinter.ttk as ttk

from awt.Event import Event
from awt.BaseWidgetMixin import BaseWidgetMixin
from awt.Action import Action
from awt.ActionEvent import ActionEvent
from awt.ActionEventProcessorMixin import ActionEventProcessorMixin
from awt.PropertyChangeEvent import PropertyChangeEvent
from awt._TkHelpers import _tk_analyze_label

class Button(ttk.Button, 
             BaseWidgetMixin, ActionEventProcessorMixin):
    """ A ttk.Button with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget = None, **kwargs):
        """
            Constructs the button.
            
            @param parent:
                The parent widget for the Button; cannot be None.
            @param kwargs:
                Keyword arguments.
        
                STANDARD OPTIONS (passed directly to ttk)
                    class, compound, cursor, image, state, style, 
                    takefocus, text, textvariable, underline, width

                WIDGET-SPECIFIC OPTIONS
                    action: the awt.Action to bind to this Button.
                            *   When the Button is pressed, the Action is invoked.
                            *   When Action's properties change, the Button 
                                appearance changes.
        """
        assert isinstance(parent, tk.BaseWidget)
        
        ttk.Button.__init__(self, 
                            parent, 
                            **Button.__filter_tk_kwargs(kwargs))
        BaseWidgetMixin.__init__(self)
        ActionEventProcessorMixin.__init__(self)

        #   Bind the newly created Button with the Action?
        action = kwargs.get('action', None)
        if isinstance(action, Action):
            self.__action = action
            (tk_text, tk_underline) = _tk_analyze_label(action.name)
            self.configure(text=tk_text, underline=tk_underline)
            self.enabled = action.enabled
            #   Link this Button with the Action
            action.add_property_change_listener(self.__on_action_property_changed)
            self.add_action_listener(action.execute)
        else:
            self.__action = None
            (tk_text, tk_underline) = _tk_analyze_label(kwargs["text"])
            self.configure(text=tk_text, underline=tk_underline)

        #   Done
        self.configure(command = self.__on_tk_click)

    ##########
    #   Operations (event processing) - normally, don't touch!
    def _process_event(self, event : Event):
        return (BaseWidgetMixin._process_event(self, event) or
                ActionEventProcessorMixin._process_event(self, event))

    ##########
    #   Implementation helpers
    @staticmethod
    def __filter_tk_kwargs(kwargs) -> dict:
        result = dict(kwargs)
        result.pop("action", None)
        result.pop("text", None)
        result.pop("command", None)
        #   TODO uncomment and implement with "default" property: result.pop("default", None)
        return result

    ##########
    #   Event listeners
    def __on_action_property_changed(self, evt: PropertyChangeEvent) -> None:
        match evt.changed_property:
            case Action.NAME_PROPERTY_NAME:
                self.label = self.__action.name
            case Action.SHORTCUT_PROPERTY_NAME:
                self.shortcut = self.__action.shortcut
            case Action.ENABLED_PROPERTY_NAME:
                self.enabled = self.__action.enabled
            case _:
                assert False    #   TODO implement other Action properties

    def __on_tk_click(self):
        evt = ActionEvent(self)
        self._process_action_event(evt)
