from typing import Callable
from inspect import signature

import awt_impl.Event
import awt_impl.ActionEvent
import awt_impl.ActionEventListener

class BaseWidgetMixin:
    """ A mix-in class that adds functionality to BaseWidgets. """

    ##########
    #   Operations
    @property    
    def is_enabled(self):
        """ True if this Button is enabled, False if disabled. """
        return tk.DISABLED in self.state()

    def enable(self, yes: bool = True):
        """
            Enables of disables this button.
            
            @param yes:
                True to enable the button, false to disable. Default is True.
        """
        if yes:
            self.state(["!disabled"])
        else:
            self.state(["disabled"])

    def disable(self):
        """ Disables this button. """
        self.enable(False)
