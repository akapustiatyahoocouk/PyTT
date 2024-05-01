""" A ttk.Notebook with AWT extensions. """
#   Python standard library
import tkinter.ttk as ttk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin

##########
#   Public entities
class TabbedPane(ttk.Notebook, 
                 BaseWidgetMixin, 
                 PropertyChangeEventProcessorMixin):
    """ A ttk.Notebook with AWT extensions. """

    ##########
    #   Constants
    __current_tab_property_name_impl = None
    @staticproperty
    def CURRENT_TAB_PROPERTY_NAME() -> str:
        """ The name of the "CURRENT_TAB" property of this tabbed pane. """
        if TabbedPane.__current_tab_property_name_impl is None:
            TabbedPane.__current_tab_property_name_impl = "CURRENT_TAB"
        return TabbedPane.__current_tab_property_name_impl

    ##########
    #   Construction
    def __init__(self, master=None, **kwargs):
        """Construct an awt TabbedPane widget with the parent master. """
        ttk.Notebook.__init__(self, master, **kwargs)
        BaseWidgetMixin.__init__(self)
        PropertyChangeEventProcessorMixin.__init__(self)
        
        #   Set up event handling
        self.bind("<<NotebookTabChanged>>", self.__on_tk_tab_changed)

    ##########
    #   Properties
    @property    
    def current_tab_index(self) -> Optional[int]:
        """ The 0-based index of the "current" tab, None if there is
            no "current" tab. """
        current_tab_name = self.select()
        if current_tab_name != "":
            return self.index(current_tab_name)
        else:
            return None
    
    @current_tab_index.setter
    def current_tab_index(self, new_index: Optional[int]) -> None:
        assert (new_index is None) or isinstance(new_index, int)
        
        if new_index is None:
            raise NotImplementedError()
        else:
            self.select(new_index)

    ##########
    #   Tk event handling    
    def __on_tk_tab_changed(self, *args):
        evt = PropertyChangeEvent(self, self, TabbedPane.CURRENT_TAB_PROPERTY_NAME)
        self.process_property_change_event(evt)
