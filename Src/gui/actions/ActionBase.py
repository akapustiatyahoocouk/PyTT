"""
    Defines the common base for all Admin skin actions.
"""
from cgitb import small
from typing import Optional
import tkinter as tk

from awt.Action import Action
from awt.KeyStroke import KeyStroke

from gui.skins.admin.MainFrame import MainFrame # TODO Acions are for all skins!

class ActionBase(Action):
    """ The common base class for all "admin" skin actions. """

    ##########
    #   Construction
    def __init__(self,
                 main_frame: MainFrame,
                 name: str,
                 hotkey: Optional[str] = None,
                 description: Optional[str] = None,
                 shortcut: Optional[KeyStroke] = None,
                 small_image: Optional[tk.PhotoImage] = None,
                 large_image: Optional[tk.PhotoImage] = None):
        Action.__init__(self, name=name, hotkey=hotkey, description=description, 
                        shortcut=shortcut, small_image=small_image, large_image=large_image)
        assert isinstance(main_frame, MainFrame)
        assert isinstance(name, str)

        self.__main_frame = main_frame

    ##########
    #   Properties
    @property
    def main_frame(self) -> "MainFrame":
        """ The MainFrame to which this Action is bound; never None. """
        return self.__main_frame
