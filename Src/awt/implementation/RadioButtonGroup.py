#   Python standard library
from typing import List
from inspect import signature
import tkinter as tk
import tkinter.ttk as ttk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .ActionEvent import ActionEvent
from .ActionEventProcessorMixin import ActionEventProcessorMixin

##########
#   Public entities
class RadioButtonGroup:

    ##########
    #   Construction
    def __init__(self):

        self.__variable = tk.IntVar(master=None, value=-1)
        self.__group_members = list()
        
    ##########
    #   Properties
    @property    
    def members(self) -> List["RadioButton"]:
        return self.__group_members.copy()
    
    ##########
    #   Operations
    def add_member(self, member: "RadioButton") -> None:
        from .RadioButton import RadioButton
        assert isinstance(member, RadioButton)
        assert member.group is None
        
        self.__group_members.append(member)
        member._RadioButton__group = self
        member._RadioButton__variable = self.__variable
        member.config(variable=self.__variable, value=len(self.__group_members) - 1)
