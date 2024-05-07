#   Python standard library
import tkinter as tk

from regex import E

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .UsersViewType import UsersViewType
from .View import View
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..misc.CurrentCredentials import CurrentCredentials
from ..dialogs.CreateUserDialog import *
from ..dialogs.ModifyUserDialog import *
from ..dialogs.DestroyUserDialog import *
from ..dialogs.CreateAccountDialog import *
from ..dialogs.ModifyAccountDialog import *
from ..dialogs.DestroyAccountDialog import *
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
class UsersView(View):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

        #   Create controls

        self.__users_tree_view = TreeView(self)
        self.__actions_panel = Panel(self)

        self.__create_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.CreateUserButton.Text"),
            image=GuiResources.image("UsersView.CreateUserButton.Image"))
        self.__modify_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.ModifyUserButton.Text"),
            image=GuiResources.image("UsersView.ModifyUserButton.Image"))
        self.__destroy_user_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.DestroyUserButton.Text"),
            image=GuiResources.image("UsersView.DestroyUserButton.Image"))

        self.__create_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.CreateAccountButton.Text"),
            image=GuiResources.image("UsersView.CreateAccountButton.Image"))
        self.__modify_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.ModifyAccountButton.Text"),
            image=GuiResources.image("UsersView.ModifyAccountButton.Image"))
        self.__destroy_account_button = Button(
            self.__actions_panel,
            text=GuiResources.string("UsersView.DestroyAccountButton.Text"),
            image=GuiResources.image("UsersView.DestroyAccountButton.Image"))

        #   Adjust controls
        self.__users_tree_view = TreeView(self, show="tree", selectmode=tk.BROWSE)
        #   TODO scrollbars

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__users_tree_view.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)

        self.__create_user_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_user_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_user_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")
        self.__create_account_button.grid(row=3, column=0, padx=0, pady=(10, 2), sticky="WE")
        self.__modify_account_button.grid(row=4, column=0, padx=0, pady=2, sticky="WE")
        self.__destroy_account_button.grid(row=5, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__users_tree_view.add_item_listener(self.__users_tree_view_listener)

        self.__create_user_button.add_action_listener(self.__on_create_user_button_clicked)
        self.__modify_user_button.add_action_listener(self.__on_modify_user_button_clicked)
        self.__destroy_user_button.add_action_listener(self.__on_destroy_user_button_clicked)
        self.__create_account_button.add_action_listener(self.__on_create_account_button_clicked)
        self.__modify_account_button.add_action_listener(self.__on_modify_account_button_clicked)
        self.__destroy_account_button.add_action_listener(self.__on_destroy_account_button_clicked)

        CurrentWorkspace.add_property_change_listener(self.__on_workspace_changed)
        Locale.add_property_change_listener(self.__on_locale_changed)
        #   TODO current credentials change
        if CurrentWorkspace.get():
            CurrentWorkspace.get().add_notification_listener(self.__on_current_workspace_modified)

    ##########
    #   Refreshable
    def refresh(self) -> None:
        credentials = CurrentCredentials.get()
        workspace = CurrentWorkspace.get()
        if (credentials is None) or (workspace is None):
            self.__users_tree_view.root_nodes.clear()
            self.__create_user_button.enabled = False
            self.__modify_user_button.enabled = False
            self.__destroy_user_button.enabled = False
            self.__create_account_button.enabled = False
            self.__modify_account_button.enabled = False
            self.__destroy_account_button.enabled = False
            return

        self.__refresh_user_nodes()

        selected_user = self.selected_user
        selected_account = self.selected_account
        try:
            can_manage_users = workspace.can_manage_users(credentials)
            #   A user should be able to modify SOME details (like
            #   real_name) of itself and SOME details (like password) of
            #   its own accounts
            mu = False if selected_user is None else selected_user.can_modify(credentials)
            ma = False if selected_account is None else selected_account.can_modify(credentials)
        except Exception:
            can_manage_users = False

        self.__create_user_button.enabled = can_manage_users
        self.__modify_user_button.enabled = (can_manage_users or mu) and (selected_user is not None)
        self.__destroy_user_button.enabled = can_manage_users and (selected_user is not None)
        self.__create_account_button.enabled = can_manage_users and (selected_user is not None)
        self.__modify_account_button.enabled = (can_manage_users or ma) and (selected_account is not None)
        self.__destroy_account_button.enabled = can_manage_users and (selected_account is not None)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return UsersViewType.instance

    @property
    def selected_object(self) -> Optional[BusinessObject]:
        node = self.__users_tree_view.current_node
        return None if node is None else node.tag

    @selected_object.setter
    def selected_object(self, obj: Optional[BusinessObject]) -> None:
        assert (obj is None) or isinstance(obj, BusinessObject)
        self.perform_refresh()
        if obj is None:
            return
        for user_node in self.__users_tree_view.root_nodes:
            if user_node.tag == obj:
                self.__users_tree_view.current_node = user_node
                return
            for account_node in user_node.child_nodes:
                if account_node.tag == obj:
                    self.__users_tree_view.current_node = account_node
                    return

    @property
    def selected_user(self) -> Optional[BusinessUser]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessUser) else None

    @selected_user.setter
    def selected_user(self, user: Optional[BusinessUser]) -> None:
        assert (user is None) or isinstance(user, BusinessUser)
        self.selected_object = user

    @property
    def selected_account(self) -> Optional[BusinessAccount]:
        obj = self.selected_object
        return obj if isinstance(obj, BusinessAccount) else None

    @selected_account.setter
    def selected_account(self, account: Optional[BusinessAccount]) -> None:
        assert (account is None) or isinstance(account, BusinessAccount)
        self.selected_object = account

    ##########
    #   Implementation helpers
    def __apply_default_locale(self) -> None:
        self.__create_user_button.text = GuiResources.string("UsersViewEditor.CreateUserButton.Text")
        self.__modify_user_button.text = GuiResources.string("UsersViewEditor.ModifyUserButton.Text")
        self.__destroy_user_button.text = GuiResources.string("UsersViewEditor.DestroyUserButton.Text")

        self.__create_account_button.text = GuiResources.string("UsersViewEditor.CreateAccountButton.Text")
        self.__modify_account_button.text = GuiResources.string("UsersViewEditor.ModifyAccountButton.Text")
        self.__destroy_account_button.text = GuiResources.string("UsersViewEditor.DestroyAccountButton.Text")

    def __refresh_user_nodes(self) -> None:
        workspace = CurrentWorkspace.get()
        credentials = CurrentCredentials.get()
        if (workspace is None) or (credentials is None):
            self.__users_tree_view.root_nodes.clear()
            return
        selected_object = self.selected_object

        #   Prepare the list of accessible BusinessUsers sorted by real_name
        users = list(workspace.get_users(credentials))
        try:
            users.sort(key=lambda u: u.get_real_name(credentials))
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the self.__users_tree_view contains a proper number
        #   of root nodes...
        while len(self.__users_tree_view.root_nodes) > len(users):
            #   Too many root nodes in the users tree
            self.__users_tree_view.root_nodes.remove_at(len(self.__users_tree_view.root_nodes) - 1)
        while len(self.__users_tree_view.root_nodes) < len(users):
            #   Too few root nodes in the users tree
            user = users[len(self.__users_tree_view.root_nodes)]
            self.__users_tree_view.root_nodes.add(user.display_name,
                                                  image=user.small_image,
                                                  tag=user)
        #   ...each representing a proper BusinessUser
        for i in range(len(users)):
            try:
                user_disabled_suffix = "" if users[i].is_enabled(credentials) else ' [disabled]'
            except Exception:
                user_disabled_suffix = ""
            user_node = self.__users_tree_view.root_nodes[i]
            user_node.text = users[i].display_name + user_disabled_suffix
            user_node.tag = users[i]
            #   ...and having proper account nodes underneath
            self.__refresh_account_nodes(user_node, users[i])

        #   Try to keep the selection
        if self.selected_object != selected_object:
            self.selected_object = selected_object

    def __refresh_account_nodes(self, user_node: TreeNode, user: BusinessUser) -> None:
        credentials = CurrentCredentials.get()
        assert (user_node is not None) and (user is not None) and (credentials is not None)

        #   Prepare the list of accessible BusinessAccounts sorted by login
        accounts = list(user.get_accounts(credentials))
        try:
            accounts.sort(key=lambda a: a.get_login(credentials))
        except Exception as ex:
            ErrorDialog.show(self, ex)
            pass    #   TODO log the exception
        #   Make sure the self.__users_tree_view contains a proper number
        #   of root nodes...
        while len(user_node.child_nodes) > len(accounts):
            #   Too many leaf nodes under the user node
            user_node.child_nodes.remove_at(len(user_node.child_nodes) - 1)
        while len(user_node.child_nodes) < len(accounts):
            #   Too gew leaf nodes under the user node
            account = accounts[len(user_node.child_nodes)]
            user_node.child_nodes.add(account.display_name,
                                      image=account.small_image,
                                      tag=account)
        #   ...each representing a proper BusinessAccount
        for i in range(len(accounts)):
            try:
                account_disabled_suffix = "" if accounts[i].is_enabled(credentials) else ' [disabled]'
            except Exception as ex:
                account_disabled_suffix = ""
            account_node = user_node.child_nodes[i]
            account_node.text = accounts[i].display_name + account_disabled_suffix
            account_node.tag = accounts[i]

    ##########
    #   Event listeners
    def __on_workspace_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        if CurrentWorkspace.get() is not None:
            CurrentWorkspace.get().add_notification_listener(self.__on_current_workspace_modified)
        self.request_refresh()

    def __on_locale_changed(self, evt) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.__apply_default_locale()
        self.request_refresh()

    def __on_current_workspace_modified(self, evt: WorkspaceNotification) -> None:
        assert isinstance(evt, WorkspaceNotification)
        self.request_refresh()

    def __users_tree_view_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_create_user_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with CreateUserDialog(self.winfo_toplevel()) as dlg:
                dlg.do_modal()
                if dlg.result is CreateUserDialogResult.CANCEL:
                    return
                created_user = dlg.created_user
                self.selected_object = created_user
                self.__users_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)

    def __on_modify_user_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            user = self.selected_user
            with ModifyUserDialog(self.winfo_toplevel(), user) as dlg:
                dlg.do_modal()
            self.selected_user = user
            self.__users_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)

    def __on_destroy_user_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with DestroyUserDialog(self.winfo_toplevel(), self.selected_user) as dlg:
                dlg.do_modal()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)

    def __on_create_account_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        user = self.selected_user
        try:
            with CreateAccountDialog(self.winfo_toplevel(), user) as dlg:
                dlg.do_modal()
                if dlg.result is CreateAccountDialogResult.CANCEL:
                    return
                created_account = dlg.created_account
                self.selected_object = created_account
                self.__users_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)

    def __on_modify_account_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            account = self.selected_account
            with ModifyAccountDialog(self.winfo_toplevel(), account) as dlg:
                dlg.do_modal()
            self.selected_account = account
            self.__users_tree_view.focus_set()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)

    def __on_destroy_account_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        try:
            with DestroyAccountDialog(self.winfo_toplevel(), self.selected_account) as dlg:
                dlg.do_modal()
            self.request_refresh()
        except Exception as ex: #   error in ModifyUserDialog constructor
            ErrorDialog.show(None, ex)
