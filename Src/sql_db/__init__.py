print('Loading package', __file__)

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class SqlDbSubsystem(LocalizableSubsystem):
    """ The "Storage/SqlDb" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert SqlDbSubsystem.__instance_acquisition_in_progress, "Use SqlDbSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, StorageSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if SqlDbSubsystem.__instance is None:
            SqlDbSubsystem.__instance_acquisition_in_progress = True
            SqlDbSubsystem.__instance = SqlDbSubsystem()
            SqlDbSubsystem.__instance_acquisition_in_progress = False
        return SqlDbSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from sql_db.resources.SqlDbResources import SqlDbResources
        return SqlDbResources.string("SqlDbSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from sql_db.resources.SqlDbResources import SqlDbResources
        return SqlDbResources.factory.supported_locales

##########
#   Instantiate
SqlDbSubsystem.instance
