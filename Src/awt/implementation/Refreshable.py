""" Defines an interface to a generic UI object that can be 
    "refreshed", typically updating its internal state and 
    then repainting. """
#   Python standard library
import tkinter as tk
import traceback

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .GuiRoot import GuiRoot

##########
#   Public entities
class Refreshable:
    """ A generic UI object that can be "refreshed", typically
        updating its internal state and then repainting. """

    ##########
    #   Construction
    def __init__(self):
        """ Constructs the Refreshable object """
        self.__refresh_underway = False

    ##########
    #   Operations
    def request_refresh(self) -> None:
        """ Instructs this UI object that a "refresh" is required
            as soon as practicable, returning immediately. The refresh
            will typically be performed on the entire UI widgets tree,
            starting with the closest parent Toplevel. """
        refresh_root = self.__find_refresh_root()
        GuiRoot.tk.after_idle(Refreshable.__do_refresh, refresh_root)

    def perform_refresh(self) -> None:
        """ Instructs this UI object that a "refresh" is required
            right away, returning after it is done. The refresh will
            typically be performed on the entire UI widgets tree,
            starting with the closest parent Toplevel. """
        refresh_root = self.__find_refresh_root()
        Refreshable.__do_refresh(refresh_root)

    def refresh(self) -> None:
        """ Called by the refresh handling logic whenever a "refresh"
            is performed on this UI object. """
        pass

    ##########
    #   Implementation
    def __find_refresh_root(self) -> Any:
        if isinstance(self, tk.BaseWidget):
            #   Need the closest Toplevel
            if isinstance(self, tk.Toplevel):
                #   We are at a Toplevel
                return self
            if not isinstance(self.master, tk.BaseWidget):
                #   No master (parent) or it is not a tk [Base]Widget
                return self
            return self.master.__find_refresh_root()
        #   Else no point in trying to find a Toplevel
        return self

    @staticmethod
    def __do_refresh(refresh_root) -> Any:
        if isinstance(refresh_root, Refreshable):
            if not refresh_root._Refreshable__refresh_underway:
                refresh_root._Refreshable__refresh_underway = True
                try:
                    refresh_root.refresh()
                except Exception:
                    print(traceback.format_exc())
                refresh_root._Refreshable__refresh_underway = False
        if isinstance(refresh_root, tk.BaseWidget):
            for child in refresh_root.winfo_children():
                Refreshable.__do_refresh(child)
