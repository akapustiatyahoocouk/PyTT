print('Loading package', __file__)

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class WorkspaceSubsystem(LocalizableSubsystem):
    """ The "Storage/Workspace" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert WorkspaceSubsystem.__instance_acquisition_in_progress, "Use WorkspaceSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, StorageSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if WorkspaceSubsystem.__instance is None:
            WorkspaceSubsystem.__instance_acquisition_in_progress = True
            WorkspaceSubsystem.__instance = WorkspaceSubsystem()
            WorkspaceSubsystem.__instance_acquisition_in_progress = False
        return WorkspaceSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from workspace.resources.WorkspaceResources import WorkspaceResources
        return WorkspaceResources.string("WorkspaceSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from workspace.resources.WorkspaceResources import WorkspaceResources
        return WorkspaceResources.factory.supported_locales

##########
#   Instantiate
WorkspaceSubsystem.instance

