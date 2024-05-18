
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .PublicActivitiesViewType import PublicActivitiesViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from ..dialogs.CreatePublicActivityDialog import *
from ..dialogs.ModifyPublicActivityDialog import *
from ..dialogs.DestroyPublicActivityDialog import *
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class PublicActivitiesView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__public_activities_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_public_activity_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicActivitiesView.CreatePublicActivityButton.Text"),
            image=GuiResources.image("PublicActivitiesView.CreatePublicActivityButton.Image"))
        self.__modify_public_activity_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicActivitiesView.ModifyPublicActivityButton.Text"),
            image=GuiResources.image("PublicActivitiesView.ModifyPublicActivityButton.Image"))
        self.__destroy_public_activity_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicActivitiesView.DestroyPublicActivityButton.Text"),
            image=GuiResources.image("PublicActivitiesView.DestroyPublicActivityButton.Image"))

        #   Adjust controls
        self.__public_activities_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__public_activities_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__create_public_activity_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_public_activity_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_public_activity_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__public_activities_tree_view.add_item_listener(self.__public_activities_tree_view_listener)

        self.__create_public_activity_button.add_action_listener(self.__on_create_public_activity_button_clicked)
        self.__modify_public_activity_button.add_action_listener(self.__on_modify_public_activity_button_clicked)
        self.__destroy_public_activity_button.add_action_listener(self.__on_destroy_public_activity_button_clicked)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()
        if (credentials is None) or (workspace is None):
            self.__public_activities_tree_view.root_nodes.clear()
            self.__create_public_activity_button.enabled = False
            self.__modify_public_activity_button.enabled = False
            self.__destroy_public_activity_button.enabled = False
            return

        self.__refresh_public_activity_nodes()

        selected_public_activity = self.selected_public_activity
        try:
            can_manage_public_activities = workspace.can_manage_public_activities(credentials)
        except Exception:
            can_manage_public_activities = False

        self.__create_public_activity_button.enabled = can_manage_public_activities
        self.__modify_public_activity_button.enabled = can_manage_public_activities and (selected_public_activity is not None)
        self.__destroy_public_activity_button.enabled = can_manage_public_activities and (selected_public_activity is not None)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return PublicActivitiesViewType.instance

    @property
    def selected_object(self) -> Optional[BusinessObject]:
        node = self.__public_activities_tree_view.current_node
        return None if node is None else node.tag

    @selected_object.setter
    def selected_object(self, obj: Optional[BusinessObject]) -> None:
        assert (obj is None) or isinstance(obj, BusinessObject)
        self.perform_refresh()
        if obj is None:
            return
        for public_activity_node in self.__public_activities_tree_view.root_nodes:
            if public_activity_node.tag == obj:
                self.__public_activities_tree_view.current_node = public_activity_node
                return

    @property
    def selected_public_activity(self) -> Optional[BusinessPublicActivity]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessPublicActivity) else None

    @selected_public_activity.setter
    def selected_public_activity(self, public_activity: Optional[BusinessPublicActivity]) -> None:
        assert (public_activity is None) or isinstance(public_activity, BusinessPublicActivity)
        self.selected_object = public_activity

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_public_activity_button.text = GuiResources.string("PublicActivitiesViewEditor.CreatePublicActivityButton.Text")
        self.__modify_public_activity_button.text = GuiResources.string("PublicActivitiesViewEditor.ModifyPublicActivityButton.Text")
        self.__destroy_public_activity_button.text = GuiResources.string("PublicActivitiesViewEditor.DestroyPublicActivityButton.Text")

    def __refresh_public_activity_nodes(self) -> None:
        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__public_activities_tree_view.root_nodes.clear()
            return
        selected_object = self.selected_object

        #   Prepare the list of accessible BusinessPublicActivities sorted by name
        public_activities = list(workspace.get_public_activities(credentials))
        try:
            public_activities.sort(key=lambda u: u.get_name(credentials))
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the self.__public_activities_tree_view contains a proper number
        #   of root nodes...
        while len(self.__public_activities_tree_view.root_nodes) > len(public_activities):
            #   Too many root nodes in the public activities tree
            self.__public_activities_tree_view.root_nodes.remove_at(len(self.__public_activities_tree_view.root_nodes) - 1)
        while len(self.__public_activities_tree_view.root_nodes) < len(public_activities):
            #   Too few root nodes in the public activities tree
            public_activity = public_activities[len(self.__public_activities_tree_view.root_nodes)]
            self.__public_activities_tree_view.root_nodes.add(
                public_activity.display_name,
                image=public_activity.small_image,
                tag=public_activity)
        #   ...each representing a proper BusinessPublicActivity
        for i in range(len(public_activities)):
            public_activity_node = self.__public_activities_tree_view.root_nodes[i]
            public_activity_node.text = public_activities[i].display_name
            public_activity_node.tag = public_activities[i]

        #   Try to keep the selection
        if self.selected_object != selected_object:
            self.selected_object = selected_object

    ##########
    #   Event handlers
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__apply_default_locale()
        self.request_refresh()

    def __public_activities_tree_view_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_create_public_activity_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with CreatePublicActivityDialog(self.winfo_toplevel()) as dlg:
                dlg.do_modal()
                if dlg.result is CreatePublicActivityDialogResult.CANCEL:
                    return
                created_public_activity = dlg.created_public_activity
                self.selected_object = created_public_activity
                self.__public_activities_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in CreatePublicActivityDialog constructor
            ErrorDialog.show(None, ex)

    def __on_modify_public_activity_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            public_activity = self.selected_public_activity
            with ModifyPublicActivityDialog(self.winfo_toplevel(), public_activity) as dlg:
                dlg.do_modal()
            self.selected_public_activity = public_activity
            self.__public_activities_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyPublicActivityDialog constructor
            ErrorDialog.show(None, ex)

    def __on_destroy_public_activity_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with DestroyPublicActivityDialog(self.winfo_toplevel(), self.selected_public_activity) as dlg:
                dlg.do_modal()
            self.request_refresh()
        except Exception as ex: #   error in DestroyPublicActivityDialog constructor
            ErrorDialog.show(None, ex)

