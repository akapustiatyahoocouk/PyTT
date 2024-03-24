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
    def instance() -> "SqliteDbPlugin":
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

