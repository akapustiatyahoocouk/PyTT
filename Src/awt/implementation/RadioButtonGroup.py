""" A group of RadioButtons of which at most one can be
    checked at any given time. """
#   Python standard library
from typing import List
import tkinter as tk

##########
#   Public entities
class RadioButtonGroup:
    """ A group of RadioButtons of which at most one can
        be checked at any given time. """
    ##########
    #   Construction
    def __init__(self):

        self.__variable = tk.IntVar(master=None, value=-1)
        self.__group_members = []

    ##########
    #   Properties
    @property
    def members(self) -> List["RadioButton"]:
        """ An ordered list of all RadioButtons in this RadioButtonGroup. """
        return self.__group_members.copy()

    ##########
    #   Operations
    def add_member(self, member: "RadioButton") -> None:
        """
            Adds the specified RadioButton th this RadioButtonGroup.

            @param member:
                The RadioButton to add to this RadioButtonGroup. The
                RadioButton must not be already a member of another
                RadioButtonGroup.
        """
        from .RadioButton import RadioButton
        assert isinstance(member, RadioButton)
        assert member.group is None

        self.__group_members.append(member)
        member._RadioButton__group = self
        member._RadioButton__variable = self.__variable
        member.config(variable=self.__variable, value=len(self.__group_members) - 1)
