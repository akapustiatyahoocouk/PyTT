
#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .PrivateTasksViewType import PrivateTasksViewType
from .PrivateTasksViewSettings import PrivateTasksViewSettings
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
#from ..dialogs.CreatePrivateTaskDialog import *
#from ..dialogs.ModifyPrivateTaskDialog import *
#from ..dialogs.DestroyPrivateTaskDialog import *
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class PrivateTasksView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__private_tasks_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__private_tasks_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        self.__hide_completed_tasks_check_box = CheckBox(
            self,
            text=GuiResources.string("PrivateTasksView.HideCompletedTasksCheckBox.Text"))

        self.__create_private_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PrivateTasksView.CreatePrivateTaskButton.Text"),
            image=GuiResources.image("PrivateTasksView.CreatePrivateTaskButton.Image"))
        self.__modify_private_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PrivateTasksView.ModifyPrivateTaskButton.Text"),
            image=GuiResources.image("PrivateTasksView.ModifyPrivateTaskButton.Image"))
        self.__destroy_private_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PrivateTasksView.DestroyPrivateTaskButton.Text"),
            image=GuiResources.image("PrivateTasksView.DestroyPrivateTaskButton.Image"))

        #   Adjust controls
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__private_tasks_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        self.__hide_completed_tasks_check_box.pack(side=tk.BOTTOM, padx=0, pady=0, fill=tk.X)

        self.__create_private_task_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_private_task_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_private_task_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__private_tasks_tree_view.add_item_listener(self.__private_tasks_tree_view_listener)

        self.__create_private_task_button.add_action_listener(self.__on_create_private_task_button_clicked)
        self.__modify_private_task_button.add_action_listener(self.__on_modify_private_task_button_clicked)
        self.__destroy_private_task_button.add_action_listener(self.__on_destroy_private_task_button_clicked)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

        self.__hide_completed_tasks_check_box.add_action_listener(self.__on_hide_completed_tasks_check_box_clicked)

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()
        if (credentials is None) or (workspace is None):
            self.__private_tasks_tree_view.root_nodes.clear()
            self.__create_private_task_button.enabled = False
            self.__modify_private_task_button.enabled = False
            self.__destroy_private_task_button.enabled = False
            return

        self.__refresh_user_nodes()

        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__private_tasks_tree_view.root_nodes.clear()
        else:
            selected_object = self.selected_object
            try:
                self.__refresh_private_task_nodes(workspace,
                                                  credentials,
                                                  self.__public_tasks_tree_view.root_nodes,
                                                  workspace.get_root_private_tasks(credentials))
            except Exception:
                #   In case root tasks acquisition fails TODO log ?
                pass
        if self.selected_object != selected_object:
            #   Try to keep the selection
            self.selected_object = selected_object

        self.__hide_completed_tasks_check_box.checked = PrivateTasksViewSettings.hide_completed_tasks

        selected_private_task = self.selected_private_task
        try:
            can_manage_private_tasks = workspace.can_manage_private_tasks(credentials)
        except Exception:
            can_manage_private_tasks = False

        self.__create_private_task_button.enabled = can_manage_private_tasks
        self.__modify_private_task_button.enabled = can_manage_private_tasks and (selected_private_task is not None)
        self.__destroy_private_task_button.enabled = can_manage_private_tasks and (selected_private_task is not None)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return PrivateTasksViewType.instance

    @property
    def selected_object(self) -> Optional[BusinessObject]:
        node = self.__private_tasks_tree_view.current_node
        return None if node is None else node.tag

    @selected_object.setter
    def selected_object(self, obj: Optional[BusinessObject]) -> None:
        assert (obj is None) or isinstance(obj, BusinessObject)
        self.perform_refresh()
        if obj is None:
            return
        self.__set_selected_object(self.__private_tasks_tree_view.root_nodes, obj)

    @property
    def selected_private_task(self) -> Optional[BusinessPrivateTask]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessPrivateTask) else None

    @selected_private_task.setter
    def selected_private_task(self, private_task: Optional[BusinessPrivateTask]) -> None:
        assert (private_task is None) or isinstance(private_task, BusinessPrivateTask)
        self.selected_object = private_task

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_private_task_button.text = GuiResources.string("PrivateTasksViewEditor.CreatePrivateTaskButton.Text")
        self.__modify_private_task_button.text = GuiResources.string("PrivateTasksViewEditor.ModifyPrivateTaskButton.Text")
        self.__destroy_private_task_button.text = GuiResources.string("PrivateTasksViewEditor.DestroyPrivateTaskButton.Text")
        self.__hide_completed_tasks_check_box.text = GuiResources.string("PrivateTasksView.HideCompletedTasksCheckBox.Text")

    def __refresh_user_nodes(self) -> None:
        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__private_tasks_tree_view.root_nodes.clear()
            return
        selected_object = self.selected_object

        #   Prepare the list of accessible BusinessUsers sorted by real_name
        users = list(workspace.get_users(credentials))
        try:
            users.sort(key=lambda u: u.get_real_name(credentials))
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the self.__private_tasks_tree_view contains a proper number
        #   of root nodes...
        while len(self.__private_tasks_tree_view.root_nodes) > len(users):
            #   Too many root nodes in the users tree
            self.__private_tasks_tree_view.root_nodes.remove_at(len(self.__private_tasks_tree_view.root_nodes) - 1)
        while len(self.__private_tasks_tree_view.root_nodes) < len(users):
            #   Too few root nodes in the users tree
            user = users[len(self.__private_tasks_tree_view.root_nodes)]
            self.__private_tasks_tree_view.root_nodes.add(user.display_name,
                                                          image=user.small_image,
                                                          tag=user)
        #   ...each representing a proper BusinessUser
        for i in range(len(users)):
            try:
                user_disabled_suffix = "" if users[i].is_enabled(credentials) else ' [disabled]'
            except Exception:
                user_disabled_suffix = ""
            user_node = self.__private_tasks_tree_view.root_nodes[i]
            user_node.text = users[i].display_name + user_disabled_suffix
            user_node.tag = users[i]
            #   ...and having proper account nodes underneath
            self.__refresh_private_task_nodes(credentials,
                                              user_node.child_nodes,
                                              users[i].get_root_private_tasks(credentials))

        #   Try to keep the selection
        if self.selected_object != selected_object:
            self.selected_object = selected_object

    def __refresh_private_task_nodes(self,
                                     credentials: Credentials,
                                     tree_nodes: TreeNodeCollection,
                                     private_tasks: Set[BusinessPrivateTask]) -> None:
        #   Prepare the list of accessible BusinessPrivateTasks sorted by name
        private_tasks = list(private_tasks)
        if PrivateTasksViewSettings.hide_completed_tasks:
            private_tasks = list(filter(lambda t: (not t.is_completed(credentials)), private_tasks))
            
        try:
            private_tasks.sort(key=lambda u: u.display_name)
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the tree_nodes contains a proper number of nodes...
        while len(tree_nodes) > len(private_tasks):
            #   Too many nodes in the private tasks list
            tree_nodes.remove_at(len(tree_nodes) - 1)
        while len(tree_nodes) < len(private_tasks):
            #   Too few nodes in the private tasks list
            private_task = private_tasks[len(tree_nodes)]
            tree_nodes.add(private_task.display_name,
                           image=private_task.small_image,
                           tag=private_task)
        #   ...each representing a proper BusinessPrivateTask
        for i in range(len(private_tasks)):
            try:
                task_completed_prefix = '[completed] ' if private_tasks[i].is_completed(credentials) else ""
            except Exception as ex:
                task_completed_prefix = ""
            private_task_node = tree_nodes[i]
            private_task_node.text = task_completed_prefix + private_tasks[i].display_name
            private_task_node.tag = private_tasks[i]
            #   ...and having proper children
            try:
                self.__refresh_private_task_nodes(workspace,
                                                  credentials,
                                                  private_task_node.child_nodes,
                                                  private_tasks[i].get_children(credentials))
            except Exception:
                #   In case child tasks acquisition fails TODO log ?
                pass

    def __set_selected_object(self, tree_nodes: TreeNodeCollection, obj: Optional[BusinessObject]) -> bool:
        for tree_node in tree_nodes:
            if tree_node.tag == obj:
                tree_node.tree_view.current_node = tree_node
                return True
            if self.__set_selected_object(tree_node.child_nodes, obj):
                return True
        return False

    ##########
    #   Event handlers
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__apply_default_locale()
        self.request_refresh()

    def __private_tasks_tree_view_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_hide_completed_tasks_check_box_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        PrivateTasksViewSettings.hide_completed_tasks = self.__hide_completed_tasks_check_box.checked
        self.request_refresh()

    def __on_create_private_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        #try:
        #    with CreatePrivateTaskDialog(self.winfo_toplevel(),
        #                                parent_task=self.selected_private_task) as dlg:
        #        dlg.do_modal()
        #        if dlg.result is CreatePrivateTaskDialogResult.CANCEL:
        #            return
        #        created_private_task = dlg.created_private_task
        #        self.selected_object = created_private_task
        #        self.__private_tasks_tree_view.focus_set()
        #    self.request_refresh()
        #except Exception as ex: #   error in CreatePrivateTaskDialog constructor
        #    ErrorDialog.show(None, ex)

    def __on_modify_private_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        #try:
        #    private_task = self.selected_private_task
        #    with ModifyPrivateTaskDialog(self.winfo_toplevel(), private_task) as dlg:
        #        dlg.do_modal()
        #    self.selected_private_task = private_task
        #    self.__private_tasks_tree_view.focus_set()
        #    self.request_refresh()
        #except Exception as ex: #   error in ModifyPrivateTaskDialog constructor
        #    ErrorDialog.show(None, ex)

    def __on_destroy_private_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        #try:
        #    with DestroyPrivateTaskDialog(self.winfo_toplevel(), self.selected_private_task) as dlg:
        #        dlg.do_modal()
        #    self.request_refresh()
        #except Exception as ex: #   error in DestroyPrivateTaskDialog constructor
        #    ErrorDialog.show(None, ex)
