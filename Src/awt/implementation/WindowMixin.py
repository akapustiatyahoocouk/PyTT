#   Python standard library
import tkinter as tk

#   Internal dependencies on modules within the same component
from .BaseWidgetMixin import BaseWidgetMixin
from .WindowState import WindowState

##########
#   Public entities
class WindowMixin(BaseWidgetMixin):

    ##########
    #   Implementation
    __ICONIFIED_CHECK_INTERVAL_MS = 500

    ##########
    #   Construction
    def __init__(self):
        BaseWidgetMixin.__init__(self)
        
        self.bind("<Configure>", self.__on_tk_configure)
        self.__last_state = self.wm_state()
    
        self.after(WindowMixin.__ICONIFIED_CHECK_INTERVAL_MS, self.__on_tk_timer_tick)
    
    def __on_tk_timer_tick(self):
        new_state = self.wm_state()
        if new_state != self.__last_state:
            self.__last_state = new_state
            print(self, new_state, self.window_state)
        if self.winfo_exists():
            self.after(WindowMixin.__ICONIFIED_CHECK_INTERVAL_MS, self.__on_tk_timer_tick)
        
    ##########
    #   Properties
    @property
    def topmost(self):
        """ True if this is a topmost window, False if not. """
        return tk.Toplevel.attributes(self, "-topmost") == 1

    @topmost.setter
    def topmost(self, new_topmost: bool):
        """
            Makes this window topmost or not.

            @param new_topmost:
                True to make this the topmost window, False to
                make this a regular window.
        """
        assert isinstance(new_topmost, bool)
        tk.Toplevel.attributes(self, "-topmost", 1 if new_topmost else 0)

    @property
    def window_state(self) -> WindowState:
        match self.__last_state:
            case "normal":
                return WindowState.NORMAL
            case "icon":
                return WindowState.ICONIFIED
            case "iconic":
                return WindowState.ICONIFIED
            case "zoomed":
                return WindowState.MAXIMIZED
            case "withdrawn":
                return WindowState.WITHDRAWN
            case _:
                return WindowState.UNDEFINED

    @window_state.setter
    def window_state(self, new_window_state: WindowState) -> None:
        assert isinstance(new_window_state, WindowState)

        if new_window_state == self.window_state:
            return
        match new_window_state:
            case WindowState.NORMAL:
                self.__last_state = "normal"
            case WindowState.MAXIMIZED:
                self.__last_state = "zoomed"
            case WindowState.ICONIFIED:
                self.__last_state = "iconic"
            case WindowState.WITHDRAWN:
                self.__last_state = "withdrawn"
            case _:
                return
        self.wm_state([self.__last_state])

    ##########
    #   Tk event handlers
    def __on_tk_configure(self, evt: tk.Event):
        new_state = self.wm_state()
        if new_state != self.__last_state:
            self.__last_state = new_state
            print(self, new_state, self.window_state)
        return BaseWidgetMixin._BaseWidgetMixin__on_tk_configure(self, evt)
