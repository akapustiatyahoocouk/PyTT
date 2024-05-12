""" The set of actions defined by Admin skin. """

#   Python standard library
from typing import final, List

#   Internal dependencies on modules within the same component
from .CreateWorkspaceAction import CreateWorkspaceAction
from .OpenWorkspaceAction import OpenWorkspaceAction
from .CloseWorkspaceAction import CloseWorkspaceAction
from .DestroyWorkspaceAction import DestroyWorkspaceAction
from .ExitAction import ExitAction
from .ManageUsersAction import ManageUsersAction
from .ManageActivityTypesAction import ManageActivityTypesAction
from .ManagePublicActivitiesAction import ManagePublicActivitiesAction
from .ManagePrivateActivitiesAction import ManagePrivateActivitiesAction
from .LoginAsDifferentUserAction import LoginAsDifferentUserAction
from .PreferencesAction import PreferencesAction
from .HelpContentAction import HelpContentAction
from .AboutAction import AboutAction
from gui.implementation.views.ViewType import ViewType

##########
#   Public entities
@final
class ActionSet:
    """ The set of all Actions provided by the Admin skin. """

    ##########
    #   Construction
    def __init__(self):
        self.__create_workspace = CreateWorkspaceAction()
        self.__open_workspace = OpenWorkspaceAction()
        self.__close_workspace = CloseWorkspaceAction()
        self.__destroy_workspace = DestroyWorkspaceAction()
        self.__exit = ExitAction()
        self.__manage_users = ManageUsersAction()
        self.__manage_activity_types = ManageActivityTypesAction()
        self.__manage_public_activities = ManagePublicActivitiesAction()
        self.__manage_private_activities = ManagePrivateActivitiesAction()
        self.__login_as_different_user = LoginAsDifferentUserAction()
        self.__preferences = PreferencesAction()
        self.__help_content = HelpContentAction()
        self.__about = AboutAction()

    ##########
    #   Actions
    @property
    def create_workspace(self) -> ExitAction:
        """ The "Create workspace" action. """
        return self.__create_workspace

    @property
    def open_workspace(self) -> ExitAction:
        """ The "Open workspace" action. """
        return self.__open_workspace

    @property
    def close_workspace(self) -> ExitAction:
        """ The "Close workspace" action. """
        return self.__close_workspace

    @property
    def destroy_workspace(self) -> ExitAction:
        """ The "Destroy workspace" action. """
        return self.__destroy_workspace

    @property
    def exit(self) -> ExitAction:
        """ The "Exit PyTT" action. """
        return self.__exit

    @property
    def manage_users(self) -> ManageUsersAction:
        """ The "Manage users" action. """
        return self.__manage_users

    @property
    def manage_activity_types(self) -> ManageActivityTypesAction:
        """ The "Manage activity types" action. """
        return self.__manage_activity_types

    @property
    def manage_public_activities(self) -> ManagePublicActivitiesAction:
        """ The "Manage public activities" action. """
        return self.__manage_public_activities

    @property
    def manage_private_activities(self) -> ManagePrivateActivitiesAction:
        """ The "Manage private activities" action. """
        return self.__manage_private_activities

    @property
    def login_as_different_user(self) -> PreferencesAction:
        """ The "Login as a different user" action. """
        return self.__login_as_different_user

    @property
    def preferences(self) -> PreferencesAction:
        """ The "PyTT preferences" action. """
        return self.__preferences

    @property
    def help_content(self) -> HelpContentAction:
        """ The "PyTT Help Content" action. """
        return self.__help_content

    @property
    def about(self) -> AboutAction:
        """ The "About PyTT" action. """
        return self.__about
