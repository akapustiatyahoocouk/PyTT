print('Loading package', __file__)

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class DbSubsystem(LocalizableSubsystem):
    """ The "Storage/Db" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert DbSubsystem.__instance_acquisition_in_progress, "Use DbSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, StorageSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if DbSubsystem.__instance is None:
            DbSubsystem.__instance_acquisition_in_progress = True
            DbSubsystem.__instance = DbSubsystem()
            DbSubsystem.__instance_acquisition_in_progress = False
        return DbSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from db.resources.DbResources import DbResources
        return DbResources.string("DbSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from db.resources.DbResources import DbResources
        return DbResources.factory.supported_locales

##########
#   Instantiate
DbSubsystem.instance

