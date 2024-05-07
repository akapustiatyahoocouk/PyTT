
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .ActivityTypesViewType import ActivityTypesViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from ..dialogs.CreateActivityTypeDialog import *
from ..dialogs.ModifyActivityTypeDialog import *
from ..dialogs.DestroyActivityTypeDialog import *
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class ActivityTypesView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__activity_types_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.CreateActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.CreateActivityTypeButton.Image"))
        self.__modify_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.ModifyActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.ModifyActivityTypeButton.Image"))
        self.__destroy_activity_type_button = Button(
            self.__actions_panel,
            text=GuiResources.string("ActivityTypesView.DestroyActivityTypeButton.Text"),
            image=GuiResources.image("ActivityTypesView.DestroyActivityTypeButton.Image"))

        #   Adjust controls
        self.__activity_types_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__activity_types_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__create_activity_type_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_activity_type_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_activity_type_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__activity_types_tree_view.add_item_listener(self.__activity_types_tree_view_listener)

        self.__create_activity_type_button.add_action_listener(self.__on_create_activity_type_button_clicked)
        self.__modify_activity_type_button.add_action_listener(self.__on_modify_activity_type_button_clicked)
        self.__destroy_activity_type_button.add_action_listener(self.__on_destroy_activity_type_button_clicked)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()
        if (credentials is None) or (workspace is None):
            self.__activity_types_tree_view.root_nodes.clear()
            self.__create_activity_type_button.enabled = False
            self.__modify_activity_type_button.enabled = False
            self.__destroy_activity_type_button.enabled = False
            return

        self.__refresh_activity_type_nodes()

        selected_activity_type = self.selected_activity_type
        try:
            can_manage_activity_types = workspace.can_manage_stock_items(credentials)
        except Exception:
            can_manage_activity_types = False

        self.__create_activity_type_button.enabled = can_manage_activity_types
        self.__modify_activity_type_button.enabled = can_manage_activity_types and (selected_activity_type is not None)
        self.__destroy_activity_type_button.enabled = can_manage_activity_types and (selected_activity_type is not None)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return ActivityTypesViewType.instance

    @property
    def selected_object(self) -> Optional[BusinessObject]:
        node = self.__activity_types_tree_view.current_node
        return None if node is None else node.tag

    @selected_object.setter
    def selected_object(self, obj: Optional[BusinessObject]) -> None:
        assert (obj is None) or isinstance(obj, BusinessObject)
        self.perform_refresh()
        if obj is None:
            return
        for activity_type_node in self.__activity_types_tree_view.root_nodes:
            if activity_type_node.tag == obj:
                self.__activity_types_tree_view.current_node = activity_type_node
                return

    @property
    def selected_activity_type(self) -> Optional[BusinessActivityType]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessActivityType) else None

    @selected_activity_type.setter
    def selected_activity_type(self, activity_type: Optional[BusinessActivityType]) -> None:
        assert (activity_type is None) or isinstance(activity_type, BusinessActivityType)
        self.selected_object = activity_type

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.CreateActivityTypeButton.Text")
        self.__modify_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.ModifyActivityTypeButton.Text")
        self.__destroy_activity_type_button.text = GuiResources.string("ActivityTypesViewEditor.DestroyActivityTypeButton.Text")

    def __refresh_activity_type_nodes(self) -> None:
        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__activity_types_tree_view.root_nodes.clear()
            return
        selected_object = self.selected_object

        #   Prepare the list of accessible BusinessActivityTypes sorted by name
        activity_types = list(workspace.get_activity_types(credentials))
        try:
            activity_types.sort(key=lambda u: u.get_name(credentials))
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the self.__activity_types_tree_view contains a proper number
        #   of root nodes...
        while len(self.__activity_types_tree_view.root_nodes) > len(activity_types):
            #   Too many root nodes in the activity types tree
            self.__activity_types_tree_view.root_nodes.remove_at(len(self.__activity_types_tree_view.root_nodes) - 1)
        while len(self.__activity_types_tree_view.root_nodes) < len(activity_types):
            #   Too few root nodes in the activity types tree
            activity_type = activity_types[len(self.__activity_types_tree_view.root_nodes)]
            self.__activity_types_tree_view.root_nodes.add(
                activity_type.display_name,
                image=activity_type.small_image,
                tag=activity_type)
        #   ...each representing a proper BusinessActivityType
        for i in range(len(activity_types)):
            activity_type_node = self.__activity_types_tree_view.root_nodes[i]
            activity_type_node.text = activity_types[i].display_name
            activity_type_node.tag = activity_types[i]

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

    def __activity_types_tree_view_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_create_activity_type_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with CreateActivityTypeDialog(self.winfo_toplevel()) as dlg:
                dlg.do_modal()
                if dlg.result is CreateActivityTypeDialogResult.CANCEL:
                    return
                created_activity_type = dlg.created_activity_type
                self.selected_object = created_activity_type
                self.__activity_types_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in CreateActivityTypeDialog constructor
            ErrorDialog.show(None, ex)

    def __on_modify_activity_type_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            activity_type = self.selected_activity_type
            with ModifyActivityTypeDialog(self.winfo_toplevel(), activity_type) as dlg:
                dlg.do_modal()
            self.selected_activity_type = activity_type
            self.__activity_types_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyActivityTypeDialog constructor
            ErrorDialog.show(None, ex)

    def __on_destroy_activity_type_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with DestroyActivityTypeDialog(self.winfo_toplevel(), self.selected_activity_type) as dlg:
                dlg.do_modal()
            self.request_refresh()
        except Exception as ex: #   error in DestroyActivityTypeDialog constructor
            ErrorDialog.show(None, ex)
