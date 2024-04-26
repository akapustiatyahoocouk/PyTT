""" A ttk.Radiobutton with AWT extensions. """
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ActionEvent import ActionEvent
from .ActionEventProcessorMixin import ActionEventProcessorMixin
from .RadioButtonGroup import RadioButtonGroup

##########
#   Public entities
class RadioButton(ttk.Radiobutton,
                  BaseWidgetMixin,
                  ActionEventProcessorMixin):
    """ A ttk.Radiobutton with AWT extensions. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget, group: RadioButtonGroup, **kwargs):
        ttk.Radiobutton.__init__(self, parent, **kwargs)
        BaseWidgetMixin.__init__(self)
        ActionEventProcessorMixin.__init__(self)

        assert isinstance(group, RadioButtonGroup)
        self.__group = None
        self.__variable = None
        self.config(variable=None, command=self.__radiobutton_clicked)
        group.add_member(self)

    ##########
    #   Properties
    @property
    def group(self) -> RadioButtonGroup:
        """ The RadioButtonGroup to which this RadioButton belongs;
            None if this RadioButton is not assigned to a 
            RadioButtonGroup. """
        return self.__group

    @property
    def checked(self) -> bool:
        """ True if this RadioButton is currently checked, False 
            unchecked. """
        if self.__group is None:
            return False
        index = self.__group.members.index(self)
        return self.__variable.get() == index

    @checked.setter
    def checked(self, new_checked: bool) -> bool:
        """ Checks (true) or unchecks (False) this RadioButton. """
        assert isinstance(new_checked, bool)
        if self.__group is None:
            return
        index = self.__group.members.index(self)
        self.__variable.set(index)

    ##########
    #   Tk event handlers
    def __radiobutton_clicked(self):
        evt = ActionEvent(self)
        self.process_action_event(evt)
        return "break"
