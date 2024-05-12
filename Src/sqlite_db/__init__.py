from __future__ import annotations  #   MUST be 1st in a module!
print('Loading package', __file__)

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from db.interface.api import *
from pnp.interface.api import *
from util.interface.api import *

@final
class SqliteDbPlugin(Plugin):
    
    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Plugin = None

    def __init__(self):
        assert SqliteDbPlugin.__instance_acquisition_in_progress, "Use SqliteDbPlugin.instance instead"
        Plugin.__init__(self)
    
    @staticproperty
    def instance() -> SqliteDbPlugin:
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if SqliteDbPlugin.__instance is None:
            SqliteDbPlugin.__instance_acquisition_in_progress = True
            SqliteDbPlugin.__instance = SqliteDbPlugin()
            SqliteDbPlugin.__instance_acquisition_in_progress = False
        return SqliteDbPlugin.__instance

    ##########
    #   Plugin
    @property
    def display_name(self) -> str:
        return "SQLite database support"

    def initialize(self) -> None:
        from sqlite_db.implementation.SqliteDatabaseType import SqliteDatabaseType
        DatabaseType.register(SqliteDatabaseType.instance)

SqliteDbPlugin.instance

##########
#   Public entities
@final
class SqliteDbSubsystem(LocalizableSubsystem):
    """ The "Storage/Sqlite" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert SqliteDbSubsystem.__instance_acquisition_in_progress, "Use SqliteDbSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, StorageSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if SqliteDbSubsystem.__instance is None:
            SqliteDbSubsystem.__instance_acquisition_in_progress = True
            SqliteDbSubsystem.__instance = SqliteDbSubsystem()
            SqliteDbSubsystem.__instance_acquisition_in_progress = False
        return SqliteDbSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from sqlite_db.resources.SqliteDbResources import SqliteDbResources
        return SqliteDbResources.string("SqliteDbSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from sqlite_db.resources.SqliteDbResources import SqliteDbResources
        return SqliteDbResources.factory.supported_locales

##########
#   Instantiate
SqliteDbSubsystem.instance
