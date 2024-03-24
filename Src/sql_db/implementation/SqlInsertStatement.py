#   Python standard library
from typing import Any
from abc import ABC, abstractmethod

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlStatement import SqlStatement

##########
#   Public entities
class SqlInsertStatement(SqlStatement):
    """ An SQL INSERT statement, perhaps parameterised. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, sql_template: str):
        """
            Constructs the SQL INSERT statement from a 
            database-independent SQL statement template.

            @param db:
                The SqlDatabase for which this SqlUbsertStatement 
                is applicable.
            @param sql_template:
                The SQL INSERT statement template (database 
                engine - neutral).
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        SqlStatement.__init__(self, db, sql_template)

    ##########
    #   SqlStatement - Operations
    def execute(self) -> Any:
        """
            Executes this SQL INSERT statement.

            @return:
                If the primary key of the table inserted into is
                an INTEGER AUTOINCREMENT, then the PK of the table 
                row insered by this stamenent; else None.
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        try:
            return self.database.execute_sql(self.prepared_sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)
