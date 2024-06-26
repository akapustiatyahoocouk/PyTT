""" An SQL UPDATE statement, perhaps parameterised. """

#   Python standard library
from typing import Any
from abc import ABC, abstractmethod

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDatabase import SqlDatabase
from .SqlStatement import SqlStatement
from .SqlRecordSet import SqlRecordSet

##########
#   Public entities
class SqlUpdateStatement(SqlStatement):
    """ An SQL UPDATE statement, perhaps parameterised. """

    ##########
    #   Construction - internal only
    def __init__(self, db: SqlDatabase, sql_template: str):
        """
            Constructs the SQL UPDATE statement from a 
            database-independent SQL statement template.

            @param db:
                The SqlDatabase for which this SqlUbsertStatement 
                is applicable.
            @param sql_template:
                The SQL UPDATE statement template (database 
                engine - neutral).
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        SqlStatement.__init__(self, db, sql_template)

    ##########
    #   SqlStatement - Operations
    def execute(self) -> int:
        """
            Executes this SQL UPDATE statement.

            @return:
                The number of rows aggected by the update.
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        try:
            return self.database.execute_sql(self.prepared_sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError.wrap(ex)
