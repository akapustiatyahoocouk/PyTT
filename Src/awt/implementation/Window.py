#   Python standard library
from typing import final, Optional, Union
import tkinter

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .GuiRoot import GuiRoot
from .BaseWidgetMixin import BaseWidgetMixin
from .MenuBar import MenuBar
from .WindowState import WindowState
from .WindowEvent import WindowEvent
from .WindowEventType import WindowEventType
from .WindowEventListener import WindowEventListener
from .WindowEventHandler import WindowEventHandler

##########
#   Public entities
@final
class Window(tkinter.Toplevel, BaseWidgetMixin):
    """ The generic top-level UI window. """

    ##########
    #   Implementation
    __ICONIFIED_CHECK_INTERVAL_MS = 500

    ##########
    #   Construction
    def __init__(self, parent: Optional[tkinter.BaseWidget] = None, title: str = GuiRoot.tk.title()):
        """ Constructs a top-level window. """
        if parent is None:
            parent = GuiRoot.tk
        tkinter.Toplevel.__init__(self, parent)
        BaseWidgetMixin.__init__(self)

        assert isinstance(parent, Window) or (parent is GuiRoot.tk)
        assert isinstance(title, str)

        self.__menu_bar = None
        self.__icon = None

        #TODO kill off self.state("withdrawn")
        self.title(title)

        #   Set up event handlers
        #   TODO make list elements WEAK references to actual listeners
        self.__window_listeners = list()

        self.bind("<Configure>", self.__on_tk_configure)
        self.protocol("WM_DELETE_WINDOW", self.__on_tk_delete_window)

        self.__last_state = self.wm_state()
        self.after(Window.__ICONIFIED_CHECK_INTERVAL_MS, self.__on_tk_timer_tick)

    ##########
    #   tkinter support
    def tk(self) -> tkinter.Tk:
        return self.__tk

    ##########
    #   tkinter.Wm
    def attributes(self, *args):
        raise NotImplementedError("Use AWT-defined properties instead")

    ##########
    #   Properties
    @property
    def menu_bar(self) -> Optional[MenuBar]:
        return self.__menu_bar

    @menu_bar.setter
    def menu_bar(self, new_menu_bar: Optional[MenuBar]) -> None:
        assert (new_menu_bar is None) or isinstance(new_menu_bar, MenuBar)

        if new_menu_bar is self.__menu_bar:
            return  #   Already there
        if new_menu_bar is None:
            if self.__menu_bar is not None:
                self.__menu_bar._Menu__tk_impl.master = None
            self["menu"] = ""
            self.__menu_bar = None
        else:
            assert isinstance(new_menu_bar, Optional[MenuBar])
            new_menu_bar._Menu__tk_impl.master._impl = self
            self["menu"] = new_menu_bar._Menu__tk_impl
            self.__menu_bar = new_menu_bar

    @property
    def icon(self) -> Optional[tkinter.PhotoImage]:
        return self.__icon

    @icon.setter
    def icon(self, new_icon: Optional[tkinter.PhotoImage]) -> None:
        assert (new_icon is None) or isinstance(new_icon , tkinter.PhotoImage)
        if new_icon is self.__icon:
            return
        if new_icon is None:
            self.wm_iconphoto(False, None)
        else:
            self.wm_iconphoto(False, new_icon)
        self.__icon = new_icon

    ##########
    #   Properties
    @property
    def topmost(self):
        """ True if this is a topmost window, False if not. """
        return tkinter.Toplevel.attributes(self, "-topmost") == 1

    @topmost.setter
    def topmost(self, new_topmost: bool):
        """
            Makes this window topmost or not.

            @param new_topmost:
                True to make this the topmost window, False to
                make this a regular window.
        """
        assert isinstance(new_topmost, bool)
        tkinter.Toplevel.attributes(self, "-topmost", 1 if new_topmost else 0)

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
        self.state(self.__last_state)

    ##########
    #   Operations
    def add_window_listener(self, l: Union[WindowEventListener, WindowEventHandler]) -> None:
        """ Registers the specified listener or handler to be notified when
            a window event is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WindowEventHandler))
        if l not in self.__window_listeners:
            self.__window_listeners.append(l)

    def remove_window_listener(self, l: Union[WindowEventListener, WindowEventHandler]) -> None:
        """ Un-regosters the specified listener or handler to no longer be
            notified when a window event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WindowEventHandler))
        if l in self.__window_listeners:
            self.__window_listeners.remove(l)

    @property
    def window_listeners(self) -> list[Union[WindowEventListener, WindowEventHandler]]:
        """ The list of all window event listeners and handlers
            registered so far. """
        return self.__window_listeners.copy()

    def process_window_event(self, event : WindowEvent) -> bool:
        """
            Called to process a WindowEvent.

            @param self:
                The Window on which the method has been called.
            @param event:
                The window event to process.
            @return:
                True if the event was processed, else false.
        """
        assert isinstance(event, WindowEvent)
        for l in self.window_listeners:
            try:
                if isinstance(l, WindowEventHandler):
                    match event.event_type:
                        case WindowEventType.WINDOW_MINIMIZED:
                            l.on_window_minimized(event)
                        case WindowEventType.WINDOW_MAXIMIZED:
                            l.on_window_maximized(event)
                        case WindowEventType.WINDOW_RESTORED:
                            l.on_window_restored(event)
                        case WindowEventType.WINDOW_CLOSING:
                            l.on_window_closing(event)
                else:
                    l(event)
            except:
                pass    #   TODO log the exception
        return event.processed

    ##########
    #   Implementation helpers
    def __process_window_state_change(self) -> None:
        match self.window_state:
            case WindowState.UNDEFINED:
                return
            case WindowState.NORMAL:
                evt = WindowEvent(self, WindowEventType.WINDOW_RESTORED)
            case WindowState.MAXIMIZED:
                evt = WindowEvent(self, WindowEventType.WINDOW_MAXIMIZED)
            case WindowState.ICONIFIED:
                evt = WindowEvent(self, WindowEventType.WINDOW_MINIMIZED)
            case WindowState.WITHDRAWN:
                return
        self.process_window_event(evt)

    ######
    #   Tk event handling
    def __on_tk_timer_tick(self):
        new_state = self.wm_state()
        if new_state != self.__last_state:
            self.__last_state = new_state
            #TODO kill off print(self, new_state, self.window_state)
            self.__process_window_state_change()
        if self.winfo_exists():
            self.after(Window.__ICONIFIED_CHECK_INTERVAL_MS, self.__on_tk_timer_tick)

    def __on_tk_configure(self, evt: tkinter.Event):
        new_state = self.wm_state()
        if new_state != self.__last_state:
            self.__last_state = new_state
            #TODO kill off print(self, new_state, self.window_state)
            self.__process_window_state_change()
        return BaseWidgetMixin._BaseWidgetMixin__on_tk_configure(self, evt)

    def __on_tk_delete_window(self, *args):
        evt = WindowEvent(self, WindowEventType.WINDOW_CLOSING)
        if not self.process_window_event(evt):
            #   Default outcome is destroy the window
            self.destroy()
