#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import sqlite3

#   Dependencies on other PyTT components
from db.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .SqliteDatabaseAddress import SqliteDatabaseAddress

##########
#   Public entities
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
    __instance_acquisition_in_progress = False
    __instance : DatabaseType = None

    def __init__(self):
        assert SqliteDatabaseType.__instance_acquisition_in_progress, "Use SqliteDatabaseType.instance() instead"
        DatabaseType.__init__(self)
    
    @staticproperty
    def instance() -> "SqliteDatabaseType":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if SqliteDatabaseType.__instance is None:
            SqliteDatabaseType.__instance_acquisition_in_progress = True
            SqliteDatabaseType.__instance = SqliteDatabaseType()
            SqliteDatabaseType.__instance_acquisition_in_progress = False
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
    #   DatabaseType - Database address handling
    def parse_database_address(self, external_form: str) -> DatabaseAddress:
        assert external_form is not None
        return db.sqlite_impl.SqliteDatabaseAddress.SqliteDatabaseAddress(external_form)

    @property    
    def default_database_address(self) -> DatabaseAddress:
        return None #   SQLite has no concept of a "default" database

    def enter_new_database_address(self, parent: tk.BaseWidget) -> DatabaseAddress:
        file_name = filedialog.asksaveasfilename(
            parent=parent.winfo_toplevel(),
            title='Create SQLite database',
            confirmoverwrite=False, #   create_database() will fail if file is there
            initialdir=None,    #   TODO last used UI directory
            filetypes=(('SQLite PyTT files', SqliteDatabaseType.PREFERRED_EXTENSION), 
                       ('All files', ".*")),
            defaultextension=SqliteDatabaseType.PREFERRED_EXTENSION)
        return SqliteDatabaseAddress(file_name) if file_name else None

    ##########
    #   Database handling
    def create_database(self, address: DatabaseAddress) -> Database:
        from .SqliteDatabase import SqliteDatabase
        
        if not isinstance(address, SqliteDatabaseAddress):
            raise InvalidDatabaseAddressError()
        path = address._SqliteDatabaseAddress__path  #   TODO try using "friends"
        return SqliteDatabase(address, True)
