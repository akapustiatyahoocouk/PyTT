"""
    Defines a Button - a clickable UI element.
"""
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .Action import Action
from .ActionEvent import ActionEvent
from .ActionEventProcessorMixin import ActionEventProcessorMixin

##########
#   Public entities
class Button(ttk.Button,
             BaseWidgetMixin,
             ActionEventProcessorMixin):
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
            tk_text = action.name
            try:
                tk_underline = action.name.lower().index(action.hotkey.lower())
            except:
                tk_underline = None
            tk_image = kwargs["image"] if "image" in kwargs else action.small_image

            self.configure(text=tk_text, underline=tk_underline,
                           image=tk_image, compound=tk.LEFT)
            self.enabled = action.enabled
            #   Link this Button with the Action
            action.add_property_change_listener(self.__on_action_property_changed)
            self.add_action_listener(action.execute)
        else:
            self.__action = None
            tk_text = kwargs["text"]
            tk_underline = None # TODO hotkey ?
            tk_image = kwargs.get("image", None)
            self.configure(text=tk_text, underline=tk_underline,
                           image=tk_image, compound=tk.LEFT)

        #   Done
        self.configure(command = self.__on_tk_click)

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

    ##########
    #   Tk event handlers
    def __on_tk_click(self):
        evt = ActionEvent(self)
        self.process_action_event(evt)
        return "break"
