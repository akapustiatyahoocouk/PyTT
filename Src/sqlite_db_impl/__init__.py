from typing import final

print('Loading package', __file__)

from annotations import staticproperty
import pnp_impl.Plugin

@final
class SqliteDbPlugin(pnp_impl.Plugin.Plugin):
    
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
        import db_impl.DatabaseTypeRegistry
        import sqlite_db_impl.SqliteDatabaseType
        db_impl.DatabaseTypeRegistry.DatabaseTypeRegistry.register_database_type(
            sqlite_db_impl.SqliteDatabaseType.SqliteDatabaseType.instance)

SqliteDbPlugin.instance

