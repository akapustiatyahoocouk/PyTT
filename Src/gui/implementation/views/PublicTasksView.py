
#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .PublicTasksViewType import PublicTasksViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from ..dialogs.CreatePublicTaskDialog import *
#TODO uncomment from ..dialogs.ModifyPublicTaskDialog import *
#TODO uncomment from ..dialogs.DestroyPublicTaskDialog import *
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class PublicTasksView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__public_tasks_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_public_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicTasksView.CreatePublicTaskButton.Text"),
            image=GuiResources.image("PublicTasksView.CreatePublicTaskButton.Image"))
        self.__modify_public_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicTasksView.ModifyPublicTaskButton.Text"),
            image=GuiResources.image("PublicTasksView.ModifyPublicTaskButton.Image"))
        self.__destroy_public_task_button = Button(
            self.__actions_panel,
            text=GuiResources.string("PublicTasksView.DestroyPublicTaskButton.Text"),
            image=GuiResources.image("PublicTasksView.DestroyPublicTaskButton.Image"))

        #   Adjust controls
        self.__public_tasks_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__public_tasks_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__create_public_task_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_public_task_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_public_task_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__public_tasks_tree_view.add_item_listener(self.__public_tasks_tree_view_listener)

        self.__create_public_task_button.add_action_listener(self.__on_create_public_task_button_clicked)
        self.__modify_public_task_button.add_action_listener(self.__on_modify_public_task_button_clicked)
        self.__destroy_public_task_button.add_action_listener(self.__on_destroy_public_task_button_clicked)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()
        if (credentials is None) or (workspace is None):
            self.__public_tasks_tree_view.root_nodes.clear()
            self.__create_public_task_button.enabled = False
            self.__modify_public_task_button.enabled = False
            self.__destroy_public_task_button.enabled = False
            return

        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__public_tasks_tree_view.root_nodes.clear()
        else:
            selected_object = self.selected_object
            try:
                self.__refresh_public_task_nodes(workspace,
                                                 credentials,
                                                 self.__public_tasks_tree_view.root_nodes,
                                                 workspace.get_root_public_tasks(credentials))
            except Exception:
                #   In case root tasks acquisition fails TODO log ?
                pass
        if self.selected_object != selected_object:
            #   Try to keep the selection
            self.selected_object = selected_object

        selected_public_task = self.selected_public_task
        try:
            can_manage_public_tasks = workspace.can_manage_public_tasks(credentials)
        except Exception:
            can_manage_public_tasks = False

        self.__create_public_task_button.enabled = can_manage_public_tasks
        self.__modify_public_task_button.enabled = can_manage_public_tasks and (selected_public_task is not None)
        self.__destroy_public_task_button.enabled = can_manage_public_tasks and (selected_public_task is not None)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return PublicTasksViewType.instance

    @property
    def selected_object(self) -> Optional[BusinessObject]:
        node = self.__public_tasks_tree_view.current_node
        return None if node is None else node.tag

    @selected_object.setter
    def selected_object(self, obj: Optional[BusinessObject]) -> None:
        assert (obj is None) or isinstance(obj, BusinessObject)
        self.perform_refresh()
        if obj is None:
            return
        self.__set_selected_object(self.__public_tasks_tree_view.root_nodes, obj)

    @property
    def selected_public_task(self) -> Optional[BusinessPublicTask]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessPublicTask) else None

    @selected_public_task.setter
    def selected_public_task(self, public_task: Optional[BusinessPublicTask]) -> None:
        assert (public_task is None) or isinstance(public_task, BusinessPublicTask)
        self.selected_object = public_task

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_public_task_button.text = GuiResources.string("PublicTasksViewEditor.CreatePublicTaskButton.Text")
        self.__modify_public_task_button.text = GuiResources.string("PublicTasksViewEditor.ModifyPublicTaskButton.Text")
        self.__destroy_public_task_button.text = GuiResources.string("PublicTasksViewEditor.DestroyPublicTaskButton.Text")

    def __refresh_public_task_nodes(self,
                                    workspace: Workspace,
                                    credentials: Credentials,
                                    tree_nodes: TreeNodeCollection,
                                    public_tasks: Set[BusinessPublicTask]) -> None:
        #   Prepare the list of accessible BusinessPublicTasks sorted by name
        public_tasks = list(public_tasks)
        try:
            public_tasks.sort(key=lambda u: u.display_name)
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the tree_nodes contains a proper number of nodes...
        while len(tree_nodes) > len(public_tasks):
            #   Too many nodes in the public tasks list
            tree_nodes.remove_at(len(tree_nodes) - 1)
        while len(tree_nodes) < len(public_tasks):
            #   Too few nodes in the public tasks list
            public_task = public_tasks[len(tree_nodes)]
            tree_nodes.add(public_task.display_name,
                           image=public_task.small_image,
                           tag=public_task)
        #   ...each representing a proper BusinessPublicTask
        for i in range(len(public_tasks)):
            public_task_node = tree_nodes[i]
            public_task_node.text = public_tasks[i].display_name    #   TODO + "completed" suffix
            public_task_node.tag = public_tasks[i]
            #   ...and having proper children
            try:
                self.__refresh_public_task_nodes(workspace,
                                                 credentials,
                                                 public_task_node.child_nodes,
                                                 public_tasks[i].get_children(credentials))
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

    def __public_tasks_tree_view_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_create_public_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with CreatePublicTaskDialog(self.winfo_toplevel(),
                                        parent_task=self.selected_public_task) as dlg:
                dlg.do_modal()
                if dlg.result is CreatePublicTaskDialogResult.CANCEL:
                    return
                created_public_task = dlg.created_public_task
                self.selected_object = created_public_task
                self.__public_tasks_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in CreatePublicTaskDialog constructor
            ErrorDialog.show(None, ex)

    def __on_modify_public_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        #try:
        #    public_task = self.selected_public_task
        #    with ModifyPublicTaskDialog(self.winfo_toplevel(), public_task) as dlg:
        #        dlg.do_modal()
        #    self.selected_public_task = public_task
        #    self.__public_tasks_tree_view.focus_set()
        #    self.request_refresh()
        #except Exception as ex: #   error in ModifyPublicTaskDialog constructor
        #    ErrorDialog.show(None, ex)

    def __on_destroy_public_task_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        #try:
        #    with DestroyPublicTaskDialog(self.winfo_toplevel(), self.selected_public_task) as dlg:
        #        dlg.do_modal()
        #    self.request_refresh()
        #except Exception as ex: #   error in DestroyPublicTaskDialog constructor
        #    ErrorDialog.show(None, ex)

