""" A mixin for all tk.BaseWidgets that makes them AWT-friendly. """
#   Python standard library
import tkinter as tk

#   Internal dependencies on modules within the same component
from .KeyEvent import KeyEvent, KeyEventType
from .KeyEventProcessorMixin import KeyEventProcessorMixin
from .WidgetEvent import WidgetEvent
from .WidgetEventType import WidgetEventType
from .WidgetEventProcessorMixin import WidgetEventProcessorMixin
from .Refreshable import Refreshable

##########
#   Public entities
class BaseWidgetMixin(KeyEventProcessorMixin,
                      WidgetEventProcessorMixin,
                      Refreshable):
    """ A mix-in class that adds functionality to BaseWidgets. """

    ##########
    #   Construction
    def __init__(self):
        """ The class constructor - DON'T FORGET to call from the
            constructors of the derived classes that implement
            this mixin. """
        KeyEventProcessorMixin.__init__(self)
        WidgetEventProcessorMixin.__init__(self)
        Refreshable.__init__(self)

        self.__visible = True
        self.__focusable = True
        self.configure(takefocus=1)

        self.bind("<KeyPress>", self.__on_tk_keydown)
        self.bind("<KeyRelease>", self.__on_tk_keyup)
        self.bind("<Configure>", self.__on_tk_configure)
        self.bind("<Map>", self.__on_tk_map)
        self.bind("<Unmap>", self.__on_tk_unmap)

        self.__last_x = self.winfo_x()
        self.__last_y = self.winfo_y()
        self.__last_width = self.winfo_width()
        self.__last_height = self.winfo_height()

    ##########
    #   Properties
    @property
    def visible(self):
        """ True if this widget is visible, False if hidden. """
        return self.__visible

    @visible.setter
    def visible(self, new_visible: bool):
        """
            Shows or hides this widget.

            @param new_visible:
                True to show this widget, false to hide.
        """
        assert isinstance(new_visible, bool)
        if new_visible != self.__visible:
            self.__visible = new_visible
            if new_visible:
                self.pack()
            else:
                self.pack_forget()

    @property
    def showing(self):
        """ True if this widget is visible as well as all
            its direct or indirect parent, False if hidden. """
        return self.winfo_viewable()

    @property
    def enabled(self):
        """ True if this widget is enabled, False if disabled. """
        return tk.DISABLED not in self.state()

    @enabled.setter
    def enabled(self, yes: bool):
        """
            Enables or disables this widget.

            @param value:
                True to enable this widget, false to disable.
        """
        if yes:
            self.state(["!disabled"])
        else:
            self.state(["disabled"])

    @property
    def focusable(self) -> bool:
        """ True if this worget is capable of receiving keyboard 
            input focus, False if not. """
        return self.__focusable

    @focusable.setter
    def focusable(self, new_focusable: bool) -> None:
        """ Specifies whether this widget is capable of receiving 
            keyboard input focus (True), or not (if False). """
        assert isinstance(new_focusable, bool)
        if new_focusable != self.__focusable:
            self.__focusable = new_focusable
            self.configure(takefocus=1 if new_focusable else 0)

    ##########
    #   Operations
    def center_in_parent(self) -> None:
        """ Centers this widget in within its immediate parent, or the
            screen if this widget has no parent or its parent is Tk.tk. """
        if isinstance(self.parent, tk.Tk):
            self.center_in_screen()
        else:
            w = self.winfo_width()
            h = self.winfo_height()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            px = self.parent.winfo_x()
            py = self.parent.winfo_y()
            x = px + int(pw/2) - int(w/2)
            y = py + int(ph/2) - int(h/2)
            #   TODO Try to keep the dialog within screen boundaries
            self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def center_in_screen(self) -> None:
        """ Centers this widget relative to the window where it appears. """
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int(sw/2) - int(w/2)
        y = int(sh/2) - int(h/2)
        #   TODO Try to keep the dialog within screen boundaries
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    ##########
    #   Tk event handlers
    def __on_tk_keydown(self, tk_evt: tk.Event):
        #TODO kill off print(tk_evt)
        ke = KeyEvent(self, KeyEventType.KEY_DOWN, tk_evt)
        self.process_key_event(ke)
        if ke.keychar is not None:
            ce = KeyEvent(self, KeyEventType.KEY_CHAR, tk_evt)
            self.process_key_event(ce)

    def __on_tk_keyup(self, tk_evt: tk.Event):
        #TODO kill off print(tk_evt)
        ke = KeyEvent(self, KeyEventType.KEY_UP, tk_evt)
        self.process_key_event(ke)

    def __on_tk_configure(self, tk_evt: tk.Event):
        #TODO kill off print(self, tk_evt)
        moved = ((self.__last_x != tk_evt.x) or (self.__last_y != tk_evt.y) and
                 self.__last_width == tk_evt.width and self.__last_height == tk_evt.height)
        sized = (self.__last_width != tk_evt.width or self.__last_height != tk_evt.height)
        self.__last_x = tk_evt.x
        self.__last_y = tk_evt.y
        self.__last_width = tk_evt.width
        self.__last_height = tk_evt.height
        if moved:
            evt = WidgetEvent(self, WidgetEventType.WIDGET_MOVED)
            self.process_widget_event(evt)
        if sized:
            evt = WidgetEvent(self, WidgetEventType.WIDGET_RESIZED)
            self.process_widget_event(evt)
        return "break"

    def __on_tk_map(self, tk_evt: tk.Event) -> None:
        assert isinstance(tk_evt, tk.Event)
        evt = WidgetEvent(self, WidgetEventType.WIDGET_SHOWN)
        self.process_widget_event(evt)
        return "break"

    def __on_tk_unmap(self, tk_evt: tk.Event) -> None:
        assert isinstance(tk_evt, tk.Event)
        evt = WidgetEvent(self, WidgetEventType.WIDGET_HIDDEN)
        self.process_widget_event(evt)
        return "break"
