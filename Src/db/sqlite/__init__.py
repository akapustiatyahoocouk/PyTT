print('Loading package', __file__)

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from pnp.api import *
from util.api import *

@final
class SqliteDbPlugin(Plugin):
    
    ##########
    #   Singleton
    __instance : "SqliteDbPlugin" = None

    def __init__(self):
        assert SqliteDbPlugin.__instance is None, "Use SqliteDbPlugin.instance instead"
        super().__init__()
    
    @staticproperty
    def instance() -> "SqliteDbPlugin":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if SqliteDbPlugin.__instance is None:
            SqliteDbPlugin.__instance = SqliteDbPlugin()
        return SqliteDbPlugin.__instance

    ##########
    #   Plugin
    @property
    def display_name(self) -> str:
        return "SQLite database support"

    def initialize(self) -> None:
        from db.DatabaseType import DatabaseType
        from db.sqlite.SqliteDatabaseType import SqliteDatabaseType
        DatabaseType.register(SqliteDatabaseType.instance)

SqliteDbPlugin.instance

