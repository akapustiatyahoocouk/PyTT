#   Python standard library
from time import sleep
from typing import final
import re

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .AdminSkinSettings import AdminSkinSettings
from admin_skin.resources.AdminSkinResources import AdminSkinResources

##########
#   Public entities
@final
class AdminSkinMainFrame(Frame,
                         WidgetEventHandler,
                         WindowEventHandler):
    """ The main frame of the "Admin" skin. """

    def __init__(self, title=AdminSkinResources.string("MainFrame.Title")):
        Frame.__init__(self)
        WidgetEventHandler.__init__(self)
        WindowEventHandler.__init__(self)

        from gui.implementation.actions.ActionSet import ActionSet
        self.__action_set = ActionSet()

        file_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         "FileMenu")
        file_menu.items.add(self.__action_set.create_workspace)
        file_menu.items.add(self.__action_set.open_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.close_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.destroy_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.exit)

        help_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         "HelpMenu")
        help_menu.items.add('Help', hotkey="H")
        help_menu.items.add('Search', hotkey="S").enabled = False
        help_menu.items.add('Index', hotkey="I")
        help_menu.items.add_seperator()
        help_menu.items.add(self.__action_set.about)

        menu_bar = MenuBar()
        menu_bar.items.add(file_menu)
        menu_bar.items.add(help_menu)

        self.menu_bar = menu_bar

        #   Create controls
        self.__aboutButton = Button(self, action=self.__action_set.about)
        self.__quitButton = Button(self, action=self.__action_set.exit)

        #self.menu_bar = None

        #self.__menu_bar = tk.Menu(self)
        #self["menu"] = self.__menu_bar

        #self.__file_menu = tk.Menu(tearoff=False)
        #self.__help_menu = tk.Menu(tearoff=False)
        #self.__menu_bar.add_cascade(label='File', underline=0, menu=self.__file_menu)

        #self.__menu_bar.add_cascade(label='Help', underline=0, menu=self.__help_menu)
        #self.__help_menu.add_command(label='About', underline=1, accelerator="Ctrl+F1", command=self.__popup)

        #   Set up control structure
        self.__aboutButton.pack()
        self.__quitButton.pack()

        #   Restore position & state
        self.__load_position()

        #   Set up event handlers
        self.add_window_listener(self)
        self.add_widget_listener(self)

        self.add_key_listener(lambda e: print(e))

        Workspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)

    ##########
    #   WidgetEventHandler
    def on_widget_moved(self, evt: WidgetEvent) -> None:
        self.__save_position()

    def on_widget_resized(self, evt: WidgetEvent) -> None:
        self.__save_position()

    ##########
    #   WindowEventHandler
    def on_window_minimized(self, evt: WindowEvent) -> None:
        self.__save_position()

    def on_window_maximized(self, evt: WindowEvent) -> None:
        self.__save_position()

    def on_window_restored(self, evt: WindowEvent) -> None:
        self.__save_position()

    def on_window_closing(self, evt: WindowEvent) -> None:
        evt.processed = True
        self.__action_set.exit.execute(ActionEvent(self))

    ##########
    #   Properties
    @property
    def is_active(self) -> bool:
        return self.window_state == WindowState.NORMAL

    ##########
    #   Operations
    def activate(self): # TODO replace with a setter property for "active" ?
        self.window_state = WindowState.NORMAL
        #TODO kill off when confirmed not needed self.tkraise()
        self.focus_force()

    def deactivate(self):   # TODO replace with a setter property for "active" ?
        self.window_state = WindowState.WITHDRAWN

    ##########
    #   Implementation helpers
    def __load_position(self):
        self.geometry("%dx%d+%d+%d" % (AdminSkinSettings.main_frame_width,
                                       AdminSkinSettings.main_frame_height,
                                       AdminSkinSettings.main_frame_x,
                                       AdminSkinSettings.main_frame_y))
        if AdminSkinSettings.main_frame_maximized:
            self.window_state = WindowState.MAXIMIZED

    def __save_position(self):
        if self.window_state is WindowState.NORMAL:
            AdminSkinSettings.main_frame_maximized = False
            #   TODO move geometry parsing to Window property whose
            #   value is a tuple (x,y,width,height)
            g = self.winfo_geometry()
            find = re.search("^(-?\\d+)x(-?\\d+)([+-]?\\d+)([+-]?\\d+)$", g)
            if find:
                AdminSkinSettings.main_frame_width = int(find.group(1))
                AdminSkinSettings.main_frame_height = int(find.group(2))
                AdminSkinSettings.main_frame_x = int(find.group(3))
                AdminSkinSettings.main_frame_y = int(find.group(4))
        elif self.window_state is WindowState.MAXIMIZED:
            AdminSkinSettings.main_frame_maximized = True
            pass
        
    ##########
    #   Event listeners
    def __on_workspace_changed(self, evt) -> None:
        pass
    
    def __on_locale_changed(self, evt) -> None:
        self.title(AdminSkinResources.string("MainFrame.Title"))
        