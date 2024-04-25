""" Defines a "check box" AWT widget. """
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ActionEvent import ActionEvent
from .ActionEventProcessorMixin import ActionEventProcessorMixin

##########
#   Public entities
class CheckBox(ttk.Checkbutton,
               BaseWidgetMixin,
               ActionEventProcessorMixin):
    """ A ttk.Checkbutton with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent=None, **kwargs):
        """Construct an awt Label widget with the parent master. """
        ttk.Checkbutton.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        ActionEventProcessorMixin.__init__(self)

        self.__variable = tk.BooleanVar(self)
        self.config(variable=self.__variable, command=self.__checkbox_clicked)

    ##########
    #   Properties
    @property
    def checked(self) -> bool:
        """ True if this CheckBox is currently checked, Talse if unchecked. """
        return self.__variable.get()

    @checked.setter
    def checked(self, new_checked: bool) -> bool:
        """ Checks (True) or unchecks (False) this CheckBox, """
        assert isinstance(new_checked, bool)
        if new_checked != self.__variable.get():
            self.__variable.set(new_checked)
            self.__checkbox_clicked()

    ##########
    #   Tk event handlers
    def __checkbox_clicked(self, *args):
        evt = ActionEvent(self)
        self.process_action_event(evt)
        return "break"
