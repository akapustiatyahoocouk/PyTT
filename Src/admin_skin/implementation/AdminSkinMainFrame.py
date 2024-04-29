""" The main UI frame of the Admin skin. """
#   Python standard library
from typing import final
import re

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *
from gui.interface.api import *

#   Internal dependencies on modules within the same component
from ..resources.AdminSkinResources import AdminSkinResources
from .AdminSkinSettings import AdminSkinSettings

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

        self.__views = []   #   parallel to the self.__views_tabbed_pane
        
        self.__action_set = ActionSet()

        self.__file_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "FileMenu")
        self.__file_menu.items.add(self.__action_set.create_workspace)
        self.__file_menu.items.add(self.__action_set.open_workspace)
        self.__file_menu.items.add_seperator()
        self.__file_menu.items.add(self.__action_set.close_workspace)
        self.__file_menu.items.add_seperator()
        self.__file_menu.items.add(self.__action_set.destroy_workspace)
        self.__file_menu.items.add_seperator()
        self.__file_menu.items.add(self.__action_set.exit)

        self.__view_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "ViewMenu")

        self.__tools_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "ToolsMenu")
        self.__tools_menu.items.add(self.__action_set.preferences)

        self.__help_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "HelpMenu")
        self.__help_menu.items.add('Help', hotkey="H")
        self.__help_menu.items.add('Search', hotkey="S").enabled = False
        self.__help_menu.items.add('Index', hotkey="I")
        self.__help_menu.items.add_seperator()
        self.__help_menu.items.add(self.__action_set.about)

        self.__menu_bar = MenuBar()
        self.__menu_bar.items.add(self.__file_menu)
        self.__menu_bar.items.add(self.__view_menu)
        self.__menu_bar.items.add(self.__tools_menu)
        self.__menu_bar.items.add(self.__help_menu)

        self.menu_bar = self.__menu_bar
        self.__regenerate_dynamic_menus()
        self.__regenerate_dynamic_menus()

        #   Create controls
        self.__views_tabbed_pane = TabbedPane(self)
        self.__views_tabbed_pane.focusable = False

        #   Set up control structure
        self.__views_tabbed_pane.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)

        #   Restore position & state
        self.__load_position()

        #   Set up event handlers
        self.add_window_listener(self)
        self.add_widget_listener(self)

        #TODO kill off self.add_key_listener(lambda e: print(e))

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

        #   Done
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()

        #   Frame title
        title = AdminSkinResources.string("MainFrame.Title")
        if credentials is not None:
            title += " [" + credentials.login + "]"
        if workspace is not None:
            title += " - " + workspace.address.display_form
        self.title(title)

        #   Action availability
        self.__action_set.close_workspace.enabled = workspace is not None

    ##########
    #   WidgetEventHandler
    def on_widget_moved(self, evt: WidgetEvent) -> None:
        """ Saves frame position when it has been moved. """
        assert isinstance(evt, WidgetEvent)
        self.__save_position()

    def on_widget_resized(self, evt: WidgetEvent) -> None:
        """ Saves frame position when it has been resized. """
        assert isinstance(evt, WidgetEvent)
        self.__save_position()

    ##########
    #   WindowEventHandler
    def on_window_minimized(self, evt: WindowEvent) -> None:
        """ Saves frame position when it has been minimized. """
        assert isinstance(evt, WindowEvent)
        self.__save_position()

    def on_window_maximized(self, evt: WindowEvent) -> None:
        """ Saves frame position when it has been maximized. """
        assert isinstance(evt, WindowEvent)
        self.__save_position()

    def on_window_restored(self, evt: WindowEvent) -> None:
        """ Saves frame position when it has been restored. """
        assert isinstance(evt, WindowEvent)
        self.__save_position()

    def on_window_closing(self, evt: WindowEvent) -> None:
        """ Exits PyTT when the user attempts to close the frame. """
        assert isinstance(evt, WindowEvent)
        evt.processed = True
        self.__action_set.exit.execute(ActionEvent(self))

    ##########
    #   Operations
    def activate(self): # TODO replace with a setter property for "active" ?
        """ Activates this window, by showing/de-iconizing it
            and bringing it to front. """
        self.window_state = WindowState.NORMAL
        #TODO kill off when confirmed not needed self.tkraise()
        self.focus_force()

    def deactivate(self):   # TODO replace with a setter property for "active" ?
        """ Hides this window. """
        self.window_state = WindowState.WITHDRAWN

    def open_view(self, view_type: ViewType) -> View:
        assert isinstance(view_type, ViewType)

        #   If there already exists a view of this type in this frame...
        for i in range(len(self.__views)):
            if self.__views[i].type == view_type:
                #   ...then just select it as "current"...
                self.__views_tabbed_pane.select(i)
                return self.__views[i]
        #   ...otherwise create a new view...
        view = view_type.create_view(self.__views_tabbed_pane)
        self.__views.append(view)
        self.__views_tabbed_pane.add(view, state="normal", text=view.type.display_name)
        #   ...and select it as "current"...
        self.__views_tabbed_pane.select(len(self.__views) - 1)
        return view
    
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

    def __regenerate_dynamic_menus(self) -> None:
        #   TODO kill old self.__view_menu items
        self.__view_menu.items.clear()
        for open_view_action in self.__action_set.open_view:
            self.__view_menu.items.add(open_view_action)

    ##########
    #   Event listeners
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        #   TODO tab names of the self.__views_tabbed_pane must be 
        #   localized, because they are actually display names of view types
        #   e.g. self.__views_tabbed_pane.tab(tabWidget, text = 'myNewText')
        self.request_refresh()
