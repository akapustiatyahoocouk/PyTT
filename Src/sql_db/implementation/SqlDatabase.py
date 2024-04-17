#   Python standard library
from abc import abstractmethod

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from sql_db.implementation.SqlStatement import SqlStatement

##########
#   Public entities
@final
class SqlDatabase(Database):

    ##########
    #   Construction
    def __init__(self):
        pass

    ##########
    #   Overridables (database engine - specific)

    ##########
    #   Operations
    def execute_script(self, script: str) -> None:
        assert isinstance(script, str)

        #   First, we must break "script" into individual statements:
        #   *   Anything from -- to \n is a comment.
        #   *   Anything from /* to */ is a comment.
        #   *   Single quotes ', double quotes " and backticks ` all
        #       denote quoted identifiers/strings; comments within
        #       these are not recognized as well as other quote types.
        #   *   Statements are separated by ';'; empty statements
        #       are ignored.
        statements = list()
        quote = None
        scan = 0
        while scan < len(script):
            c = script[scan]
            if (c == "\"") and (quote is None):
                #   Opening a double-quoted string
                quote = c
                scan += 1
            elif (c == "\"") and (quote == "\""):
                #   Closing a double-quoted string
                quote = None
                scan += 1
            elif (c == "'") and (quote is None):
                #   Opening a single-quoted string
                quote = c
                scan += 1
            elif (c == "'") and (quote == "'"):
                #   Closing a single-quoted string
                quote = None
                scan += 1
            elif (c == "`") and (quote is None):
                #   Opening a backtick-quoted string
                quote = c
                scan += 1
            elif (c == "`") and (quote == "`"):
                #   Closing a backtick-quoted string
                quote = None
                scan += 1
            elif (c == "-") and (quote is None) and (scan + 1 < len(script)) and (script[scan+1] == "-"):
                #   A single-line comment - remove everything until eoln
                prescan = scan + 2
                while prescan < len(script) and script[prescan] != "\n":
                    prescan += 1
                #   The range [scan..prescan] is a comment - replace with a single space
                script = script[:scan] + " " + script[prescan + 1:]
            elif (c == "/") and (quote is None) and (scan + 1 < len(script)) and (script[scan+1] == "*"):
                #   A single-line comment - remove everything until eoln
                raise NotImplementedError()
            elif (c == ";") and (quote is None):
                #   The part [0..scan) is a statement
                statement = script[:scan]
                statements.append(statement.strip())
                script = script[scan + 1:]
                scan = 0
            else:
                #   Just a character
                scan += 1
        statement = script
        statements.append(statement.strip())

        #   Now execute all non-empty statements within a single transaction
        self.begin_transaction()    #   may throw DatabaseError
        try:
            for statement in statements:
                if len(statement) > 0:
                    self.create_statement(statement).execute()
            self.commit_transaction()
        except Exception as ex:
            try:
                self.rollback_transaction()
            except:
                pass#   TODO log
            raise ex
        pass

    @abstractmethod
    def begin_transaction(self) -> None:
        """
            Begins a new transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod
    def commit_transaction(self) -> None:
        """
            Commits the current transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod
    def rollback_transaction(self) -> None:
        """
            Rolls back the current transaction.

            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute_sql(self, sql: str) -> None:
        """
            Executes a single SQL statement, ignoring its results.
            This is useful when e.g. called from execute_script().
            The SQL script shall use the underlying database engine's
            syntax, so the preferred way of executing SQL queries and
            commands is by using the create_statement() method to
            create a SqlStatement and then call execute() on that.

            @param sql:
                A single SQL statement.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    def create_statement(self, sql_template: str) -> SqlStatement:
        """
            Creates a new "SQL statement" that can be executed as
            necessary.

            @param sql_template:
                The SQL statement template.
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        assert isinstance(sql_template, str)

        sql_template = sql_template.strip()
        #   TODO cache SqlStatements on a per-thread basis for
        #   future reuse, keyed by sql_template

        #   TODO select, insert, delete, update require their own
        #   subclasses of SqlStatement!
        sql_statement = SqlStatement(self, sql_template)    #   may raise DatabaseError

        #   Done
        return sql_statement

