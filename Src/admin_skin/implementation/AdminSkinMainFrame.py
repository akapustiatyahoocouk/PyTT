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
        self.__file_menu.items.add_separator()
        self.__file_menu.items.add(self.__action_set.close_workspace)
        self.__file_menu.items.add_separator()
        self.__file_menu.items.add(self.__action_set.destroy_workspace)
        self.__file_menu.items.add_separator()
        self.__file_menu.items.add(self.__action_set.exit)

        self.__manage_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "ManageMenu")
        self.__manage_menu .items.add(self.__action_set.manage_users)
        self.__manage_menu .items.add(self.__action_set.manage_activity_types)
        self.__manage_menu .items.add(self.__action_set.manage_public_activities)

        self.__view_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "ViewMenu")

        self.__tools_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "ToolsMenu")
        self.__tools_menu.items.add(self.__action_set.login_as_different_user)
        self.__tools_menu.items.add_separator()
        self.__tools_menu.items.add(self.__action_set.preferences)

        self.__help_menu = ResourceAwareSubmenu(AdminSkinResources.factory, "HelpMenu")
        self.__help_menu.items.add(self.__action_set.help_content)
        self.__help_menu.items.add('Search', hotkey="S").enabled = False
        self.__help_menu.items.add('Index', hotkey="I").enabled = False
        self.__help_menu.items.add_separator()
        self.__help_menu.items.add(self.__action_set.about)

        self.__menu_bar = MenuBar()
        self.__menu_bar.items.add(self.__file_menu)
        self.__menu_bar.items.add(self.__manage_menu)
        self.__menu_bar.items.add(self.__view_menu)
        self.__menu_bar.items.add(self.__tools_menu)
        self.__menu_bar.items.add(self.__help_menu)

        self.menu_bar = self.__menu_bar
        self.__regenerate_dynamic_menus()

        #   Create controls
        self.__views_tabbed_pane = TabbedPane(self)
        self.__views_tabbed_pane.focusable = False

        #   Set up control structure
        self.__views_tabbed_pane.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)

        #   Restore position & state
        self.__load_position()

        #   Restore active views
        if len(AdminSkinSettings.active_views) == 0:
            #   Open default bunch of views
            self.open_view(UsersViewType.instance, save_active_views=True)
            self.open_view(ActivityTypesViewType.instance, save_active_views=True)
        else:
            #   Re-open views from last session
            self.__load_active_views()

        #   Set up event handlers
        self.add_window_listener(self)
        self.add_widget_listener(self)

        self.__views_tabbed_pane.add_property_change_listener(self.__views_tabbed_pane_selection_changed)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        CurrentCredentials.add_property_change_listener(self.__on_credentials_changed)

        if CurrentWorkspace.get():
            CurrentWorkspace.get().add_notification_listener(self.__on_current_workspace_modified)

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

        #   Action availability - statically created actions
        self.__action_set.close_workspace.enabled = workspace is not None

        #   Action availability - dynamically created actions
        for open_view_action in self.__open_view_actions:
            open_view_action.enabled = workspace is not None
        selected_view_tab_name = self.__views_tabbed_pane.select()
        self.__close_current_view_action.enabled = ((workspace is not None) and
                                                    (selected_view_tab_name != ""))
        self.__close_all_views_action.enabled = ((workspace is not None) and
                                                 (len(self.__views) > 0))

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
    #   Properties
    @property
    def current_view(self) -> View:
        """ The View currently selected in this frame, or
            None if no view is currently selected. """
        selected_view_tab_name = self.__views_tabbed_pane.select()
        if selected_view_tab_name != "":
            selected_view_index = self.__views_tabbed_pane.index(selected_view_tab_name)
            return self.__views[selected_view_index]
        else:
            return None

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

    def open_view(self, view_type: ViewType, save_active_views: bool) -> View:
        """
            Opens a view of the specified type in this main frame and
            makes it a "current" view. If the view of the specified type
            already exists, just makes it a "current" view,

            @param view_type:
                The required view type.
            @param save_active_views:
                True to save the new "active views" info, False to not save.
            @return:
                The opened/reused view of the specified type.
        """
        assert isinstance(view_type, ViewType)
        assert isinstance(save_active_views, bool)

        #   If there already exists a view of this type in this frame...
        for i in range(len(self.__views)):
            if self.__views[i].type == view_type:
                #   ...then just select it as "current"...
                self.__views_tabbed_pane.select(i)
                return self.__views[i]
        #   ...otherwise create a new view...
        view = view_type.create_view(self.__views_tabbed_pane)
        self.__views.append(view)
        self.__views_tabbed_pane.add(
            view,
            state="normal",
            text=view.type.display_name,
            image=view_type.small_image, compound=tk.LEFT)
        #   ...select it as "current"...
        self.__views_tabbed_pane.select(len(self.__views) - 1)
        #   ...save the new "list of active views"...
        if save_active_views:
            self.__save_active_views()
        #   ...and we're done
        return view

    def close_current_view(self) -> None:
        """ Closes the "current" view in this frame (if there IS one,
            otherwise has no effect). """
        selected_view_tab_name = self.__views_tabbed_pane.select()
        if selected_view_tab_name != "":
            selected_view_index = self.__views_tabbed_pane.index(selected_view_tab_name)
            item = self.__views[selected_view_index]
            del item
            self.__views.pop(selected_view_index)
            self.__views_tabbed_pane.forget(selected_view_index)

    def close_all_views(self) -> None:
        """ Closes all views currently open in this frame. """
        self.__close_all_active_views()
        self.__save_active_views()
        self.request_refresh()

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

    def __load_active_views(self) -> None:
        active_view_types = AdminSkinSettings.active_views
        for active_view_type in active_view_types:
            self.open_view(active_view_type, save_active_views=False)
        #   Load and select the "current" view
        current_view = AdminSkinSettings.current_view
        for i in range(len(self.__views)):
            if self.__views[i].type == current_view:
                self.__views_tabbed_pane.select(i)
                break

    def __save_active_views(self) -> None:
        active_views = []
        for view in self.__views:
            active_views.append(view.type)
        AdminSkinSettings.active_views = active_views
        #   Save the "current" view too
        current_tab_index = self.__views_tabbed_pane.current_tab_index
        if current_tab_index is None:
            AdminSkinSettings.current_view = None
        else:
            AdminSkinSettings.current_view = self.__views[current_tab_index].type

    def __close_all_active_views(self) -> None:
        while len(self.__views) > 0:
            item = self.__views[0]
            del item
            self.__views.pop()
            self.__views_tabbed_pane.forget(0)

    def __regenerate_dynamic_menus(self) -> None:
        self.__view_menu.items.clear()

        class ViewOpener(Action):
            """ An agent that can open a view of a required type. """
            def __init__(self, main_frame, view_type):
                Action.__init__(self,
                                name=AdminSkinResources.string("Actions.OpenView.Name")
                                                       .format(view_type.display_name),
                                small_image=view_type.small_image,
                                large_image=view_type.large_image)
                self.__main_frame = main_frame
                self.__view_type = view_type
            def execute(self, evt: ActionEvent) -> None:
                self.__main_frame.open_view(self.__view_type, save_active_views=True)

        class CloseCurrentViewAction(ResourceAwareAction):
            """ An agent that can close the current view. """
            def __init__(self, main_frame):
                ResourceAwareAction.__init__(self, AdminSkinResources.factory, "Actions.CloseCurrentView")
                self.__main_frame = main_frame
            def execute(self, evt: ActionEvent) -> None:
                self.__main_frame.close_current_view()

        class CloseAllViewsAction(ResourceAwareAction):
            """ An agent that can close all views. """
            def __init__(self, main_frame):
                ResourceAwareAction.__init__(self, AdminSkinResources.factory, "Actions.CloseAllViews")
                self.__main_frame = main_frame
            def execute(self, evt: ActionEvent) -> None:
                self.__main_frame.close_all_views()

        all_view_types = list(ViewType.all)
        all_view_types.sort(key=lambda vt: vt.display_name)
        self.__open_view_actions = []
        for view_type in all_view_types:
            action = ViewOpener(self, view_type)
            self.__open_view_actions.append(action)
            self.__view_menu.items.add(action)

        self.__view_menu.items.add_separator()

        self.__close_current_view_action = CloseCurrentViewAction(self)
        self.__view_menu.items.add(self.__close_current_view_action)

        self.__close_all_views_action = CloseAllViewsAction(self)
        self.__view_menu.items.add(self.__close_all_views_action)

    ##########
    #   Event listeners
    def __views_tabbed_pane_selection_changed(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__save_active_views()

    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__regenerate_dynamic_menus()
        if CurrentWorkspace.get() is None:
            #   TODO save active views info and close all views
            self.__save_active_views()
            self.__close_all_active_views()
        else:
            #   Reopen all views
            self.__load_active_views()
            CurrentWorkspace.get().add_notification_listener(self.__on_current_workspace_modified)
        self.request_refresh()

    def __on_credentials_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        #TODO what?
        #self.__regenerate_dynamic_menus()
        #if CurrentWorkspace.get() is None:
        #    #   TODO save active views info and close all views
        #    self.__save_active_views()
        #    self.__close_all_active_views()
        #else:
        #    #   Reopen all views
        #    self.__load_active_views()
        #    CurrentWorkspace.get().add_notification_listener(self.__on_current_workspace_modified)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__regenerate_dynamic_menus()
        #   TODO tab names of the self.__views_tabbed_pane must be
        #   localized, because they are actually display names of view types
        #   e.g. self.__views_tabbed_pane.tab(tabWidget, text = 'myNewText')
        self.request_refresh()

    def __on_current_workspace_modified(self, evt: WorkspaceNotification) -> None:
        assert isinstance(evt, WorkspaceNotification)
        self.request_refresh()
