#   Python standard library
from typing import Optional
from abc import ABC, abstractmethod

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDataType import SqlDataType

##########
#   Public entities
class SqlStatement:
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
        self.__fragments = []   #   all fragments, str or int; in the latter case int
                                #   represents a 0-based index into the self.__parameters
        self.__parameters = []  #   only (name, type, value) parameter tuples
        fragment = ""
        scan = 0
        while scan < len(sql_template):
            c = sql_template[scan]
            if c == "'":
                #   A single-quoted string starts here - everything until 
                #   the next single quote is a string literal - but beware
                #   of '' meaning ' within a string literal and \n-style
                #   escape sequences
                value, scan = self.__parse_quoted_string(sql_template, scan, "'", "'")
                fragment += db.quote_string_literal(value)
            elif c == "\"":
                #   A double-quoted string starts here - everything until 
                #   the next double quote is a quoted identifier - but beware
                #   of "" meaning " within a quoted identifier and \n-style
                #   escape sequences
                value, scan = self.__parse_quoted_string(sql_template, scan, "\"", "\"")
                fragment += db.quote_identifier(value)
            elif c == "`":
                #   A backtick-quoted string starts here - everything until 
                #   the next backtick is a quoted identifier - but beware
                #   of `` meaning ` within a quoted identifier and \n-style
                #   escape sequences
                value, scan = self.__parse_quoted_string(sql_template, scan, "`", "`")
                fragment += db.quote_identifier(value)
            elif c == "[" :
                #   A bracket-quoted identifier starts here - everything until 
                #   the next ] is a quoted identifier
                value, scan = self.__parse_quoted_string(sql_template, scan, "[", "]")
                fragment += db.quote_identifier(value)
            elif c == "?":
                #   A parameter placeholder is discovered
                #   Must record & close the current fragment...
                if len(fragment) > 0:
                    self.__fragments.append(fragment)
                    fragment = ""
                #   If an identifier follows the "?" it becomes the parameter name
                #   TODO implement this!
                parameter_name = None
                #   ...then record the parameter
                parameter = (parameter_name, None, None)
                parameter_index = len(self.__parameters)
                self.__parameters.append(parameter)
                self.__fragments.append(parameter_index)
                #   ...then skip ? and keep going
                scan += 1
            else:
                #   Just a character to add to the current fragment
                fragment += c
                scan += 1
        self.__fragments.append(fragment)

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
                elif isinstance(fragment, int):
                    parameter = self.__parameters[fragment]
                    self.__prepared_sql += self.__db.format_parameter(parameter[1], parameter[2])
        return self.__prepared_sql

    ##########
    #   Operations
    def execute(self) -> None:
        """
            Executes this SQL statement, ignoring any results it may produce.

            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        try:
            self.__db.execute_sql(self.prepared_sql)
        except Exception as ex:
            #   TODO log ?
            raise DatabaseError(str(ex)) from ex

    def set_int_parameter(self, parameter_ref: [int|str], value: Optional[int]) -> None:
        assert isinstance(parameter_ref, str) or isinstance(parameter_ref, int)
        assert (value is None) or isinstance(value, int)

        if isinstance(parameter_ref, int):
            old_parameter = self.__parameters[parameter_ref]    #   todo handle out-of-bounds errors
            new_parameter = (old_parameter[0], SqlDataType.INTEGER, value)
            self.__parameters[parameter_ref] = new_parameter
            self.__prepared_sql = None
        else:
            raise NotImplementedError()

    def set_string_parameter(self, parameter_ref: [int|str], value: Optional[str]) -> None:
        assert isinstance(parameter_ref, str) or isinstance(parameter_ref, int)
        assert (value is None) or isinstance(value, str)

        if isinstance(parameter_ref, int):
            old_parameter = self.__parameters[parameter_ref]    #   todo handle out-of-bounds errors
            new_parameter = (old_parameter[0], SqlDataType.STRING, value)
            self.__parameters[parameter_ref] = new_parameter
            self.__prepared_sql = None
        else:
            raise NotImplementedError()

    def set_bool_parameter(self, parameter_ref: [int|str], value: Optional[bool]) -> None:
        assert isinstance(parameter_ref, str) or isinstance(parameter_ref, int)
        assert (value is None) or isinstance(value, bool)

        if isinstance(parameter_ref, int):
            old_parameter = self.__parameters[parameter_ref]    #   todo handle out-of-bounds errors
            new_parameter = (old_parameter[0], SqlDataType.BOOLEAN, value)
            self.__parameters[parameter_ref] = new_parameter
            self.__prepared_sql = None
        else:
            raise NotImplementedError()

    ##########
    #   Implementation helpers
    def __parse_quoted_string(s: str, scan: int, opening_quote: str, closing_quote: str) -> (str, int):    #   (literal,new scan)
        assert scan < len(s) and s[scan] == opening_quote
        assert (opening_quote == "'" or opening_quote == "\"" or
                opening_quote == "`" or opening_quote == "[")
        assert (closing_quote == "'" or closing_quote == "\"" or
                closing_quote == "`" or closing_quote == "]")

        result = ""
        #   Skip opening quote
        scan += 1
        #   Parse the innards
        while scan < len(s):
            if s[scan] == closing_quote:
                #   end of literal OR quote-quote
                scan += 1
                if (opening_quote == closing_quote and 
                    scan < len(s) and s[scan] == closing_quote):
                    #   Quote-quote contributes a single quote to the result
                    result += quote
                    scan += 1
                    continue
                else:
                    #   Quote ends the literal
                    scan += 1
                    return (result, scan)
            if s[scan] == "\\":
                #   An escape sequence - ignore numerics for now
                scan += 1
                if scan >= len(s):
                    raise DatabaseError("Invalid escape sequence")
                match s[scan]:
                    case "\\":
                        result += "\\"
                        scan += 1
                    case "n":
                        result += "\n"
                        scan += 1
                    case "t":
                        result += "\t"
                        scan += 1
                    case _:
                        result += s[scan]
                        scan += 1
                continue
            #   Just a character
            result += s[scan]
            scan += 1
        raise DatabaseError("Quote mismatch")
