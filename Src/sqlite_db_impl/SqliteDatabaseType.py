from util import staticproperty
from db_impl.DatabaseType import DatabaseType
from db_impl.DatabaseAddress import DatabaseAddress

class SqliteDatabaseType(DatabaseType):
    """ A database type that uses SQLite as data storage. """
    
    ##########
    #   Constants
    MNEMONIC = "sqlite"
    """ The mnemonic identifier of the SQLite PyTT database type. """

    PREFERRED_EXTENSION = ".pytt"
    """ The preferred extension for SQLite PyTT databases. """

    ##########
    #   Singleton
    __instance :  DatabaseType = None

    def __init__(self):
        assert SqliteDatabaseType.__instance is None, "Use SqliteDatabaseType.instance() instead"
    
    @staticproperty
    def instance() -> "SqliteDatabaseType":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if SqliteDatabaseType.__instance is None:
            SqliteDatabaseType.__instance = SqliteDatabaseType()
        return SqliteDatabaseType.__instance
    
    ##########
    #   DatabaseType - Properties (general)
    @property    
    def mnemonic(self) -> str:
        return SqliteDatabaseType.MNEMONIC

    @property    
    def display_name(self) -> str:
        return 'SQLite'

    ##########
    #   DatabaseType - Properties (database address handling)
    def parse_database_address(self, externa_form: str) -> "DatabaseAddress":
        assert externa_form is not None
        return db.sqlite_impl.SqliteDatabaseAddress.SqliteDatabaseAddress(externa_form)

    @property    
    def default_database_address(self) -> DatabaseAddress:
        return None #   SQLite has no concept of a "default" database
