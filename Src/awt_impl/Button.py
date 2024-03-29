from typing import Callable
from inspect import signature

import tkinter.ttk as ttk

from awt_impl.Event import Event
from awt_impl.BaseWidgetMixin import BaseWidgetMixin
from awt_impl.ActionEvent import ActionEvent
from awt_impl.ActionEventProcessorMixin import ActionEventProcessorMixin
from awt_impl._TkHelpers import _analyze_label

class Button(ttk.Button, 
             BaseWidgetMixin, ActionEventProcessorMixin):
    """ A ttk.Button with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt Button widget with the parent master. """
        ttk.Button.__init__(self, 
                            master, 
                            **Button.__filter_tk_kwargs(kwargs))
        BaseWidgetMixin.__init__(self)
        ActionEventProcessorMixin.__init__(self)

        #   Bind the newly created Button with the Action?
        self.__action : awt_impl.Action = kwargs.get('action', None)
        if self.__action is not None:
            (tk_text, tk_underline) = _analyze_label(self.__action.name)
            self.configure(text=tk_text, underline=tk_underline)
            #   TODO make Button listen to action property changes
        else:
            (tk_text, tk_underline) = _analyze_label(kwargs["text"])
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
        return result

    ##########
    #   Event listeners
    def __on_tk_click(self):
        evt = ActionEvent(self)
        if self.__action is not None:
            self.__action.execute(evt)
        self._process_action_event(evt)
