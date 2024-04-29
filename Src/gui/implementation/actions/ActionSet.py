""" The set of actions defined by Admin skin. """

#   Python standard library
from typing import final, List

#   Internal dependencies on modules within the same component
from .CreateWorkspaceAction import CreateWorkspaceAction
from .OpenWorkspaceAction import OpenWorkspaceAction
from .CloseWorkspaceAction import CloseWorkspaceAction
from .DestroyWorkspaceAction import DestroyWorkspaceAction
from .ExitAction import ExitAction
from .OpenViewAction import OpenViewAction
from .PreferencesAction import PreferencesAction
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
        all_view_types = list(ViewType.all)
        all_view_types.sort(key=lambda vt: vt.display_name)

        self.__create_workspace = CreateWorkspaceAction()
        self.__open_workspace = OpenWorkspaceAction()
        self.__close_workspace = CloseWorkspaceAction()
        self.__destroy_workspace = DestroyWorkspaceAction()
        self.__exit = ExitAction()
        
        self.__open_view = []
        for view_type in all_view_types:
            self.__open_view.append(OpenViewAction(view_type))
        self.__preferences = PreferencesAction()
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
    def open_view(self) -> List[OpenViewAction]:
        return self.__open_view.copy()

    @property
    def preferences(self) -> PreferencesAction:
        """ The "PyTT preferences" action. """
        return self.__preferences

    @property
    def about(self) -> AboutAction:
        """ The "About PyTT" action. """
        return self.__about
