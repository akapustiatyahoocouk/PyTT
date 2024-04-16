#   Python standard library
from abc import ABC, abstractmethod
from sqlite3 import DatabaseError

#   Internal dependencies on modules within the same component

##########
#   Public entities
class SqlStatement(ABC):
    """ A generic SQL statement, perhaps parameterised. """

    ##########
    #   Construction - internal only
    def __init__(self, db: "SqlDatabase", sql_template: str):
        """
            Constructs the SQL statement from a database-independent
            SQL statement template.

            @param db:
                The SqlDatabase for which this SqlStatement is applicable.
            @param sql_template:
                The SQL statement template (database engine - neutral).
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        from sql_db.implementation.SqlDatabase import SqlDatabase

        assert isinstance(db, SqlDatabase)
        assert isinstance(sql_template, str)

        self.__db = db
        self.__sql_template = sql_template
        self.__prepared_sql = None

        #   Now parse the SQL statement, converting its syntax (e.g.
        #   identifier quoting, etc.) to the database engine-specific
        #   format and recording what paremeters there are
        self.__fragments = []   #   all fragments, str or (type,value) parameter tuples
        fragment = ""
        scan = 0
        quote = None
        while scan < len(sql_template):
            c = sql_template[scan]
            if (c == "'" ) and (quote is None):
                #   A single-quoted string starts here
                raise NotImplementedError()
            elif (c == "'" ) and (quote == "'"):
                #   A single-quoted string ends here
                raise NotImplementedError()
            elif (c == "\"" ) and (quote is None):
                #   A double-quoted string starts here
                raise NotImplementedError()
            elif (c == "\"" ) and (quote == "\""):
                #   A double-quoted string ends here
                raise NotImplementedError()
            elif (c == "`" ) and (quote is None):
                #   A backtick-quoted identifier starts here
                raise NotImplementedError()
            elif (c == "`" ) and (quote == "`"):
                #   A backtick-quoted identifier ends here
                raise NotImplementedError()
            elif (c == "[" ) and (quote is None):
                #   A bracket-quoted identifier starts here
                raise NotImplementedError()
            elif (c == "]" ) and (quote == "["):
                #   A bracket-quoted identifier ends here
                raise NotImplementedError()
            elif (c == "?" ) and (quote is None):
                #   A parameter placeholder is discovered
                raise NotImplementedError()
            else:
                #   Just a character to add to the current fragment
                fragment += c
                scan += 1
        self.__fragments.append(fragment)
        if quote is not None:
            raise DatabaseError("Quote not closed: " + quote)

    ##########
    #   Properties
    @property
    def database(self) -> "SqlDatabase":
        """ The SqlDatabase to which this SqlStatement belongs. """
        return self.__db

    @property
    def sql_template(self) -> str:
        """ The template used for creation of this SQL statement. """
        return self.__sql_template

    @property
    def prepared_sql(self) -> str:
        """ The SQL statement prepared for the underlying SQL database engine. """
        if self.__prepared_sql is None:
            self.__prepared_sql = ""
            for fragment in self.__fragments:
                if isinstance(fragment, str):
                    self.__prepared_sql += fragment
                else:
                    #   TODO handle parameters
                    raise NotImplementedError()
        return self.__prepared_sql

    ##########
    #   Operations
    def execute(self) -> None:
        """
            Executes this SQL statement, ignoring any resultsit may produce.

            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        try:
            self.__db.execute_sql(self.prepared_sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex
