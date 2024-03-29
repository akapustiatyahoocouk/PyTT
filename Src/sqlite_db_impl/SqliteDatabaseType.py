from util import staticproperty
from db_impl.IDatabaseType import IDatabaseType
from db_impl.IDatabaseAddress import IDatabaseAddress

class SqliteDatabaseType(IDatabaseType):
    """ A database type that uses SQLite as data storage. """
    
    ##########
    #   Constants
    MNEMONIC = "sqlite"
    """ The mnemonic identifier of the SQLite PyTT database type. """

    PREFERRED_EXTENSION = ".pytt"
    """ The preferred extension for SQLite PyTT databases. """

    ##########
    #   Singleton
    __instance :  IDatabaseType = None

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
    #   IDatabaseType - Properties (general)
    @property    
    def mnemonic(self) -> str:
        return SqliteDatabaseType.MNEMONIC

    @property    
    def display_name(self) -> str:
        return 'SQLite'

    ##########
    #   IDatabaseType - Properties (database address handling)
    def parse_database_address(self, externa_form: str) -> "IDatabaseAddress":
        assert externa_form is not None
        return db.sqlite_impl.SqliteDatabaseAddress.SqliteDatabaseAddress(externa_form)

    @property    
    def default_database_address(self) -> IDatabaseAddress:
        return None #   SQLite has no concept of a "default" database
