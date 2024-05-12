#   Python standard library
from abc import abstractmethod
from weakref import WeakValueDictionary
import hashlib

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlStatement import SqlStatement
from .SqlDataType import SqlDataType

##########
#   Public entities
@final
class SqlDatabase(Database):

    ##########
    #   Construction
    def __init__(self):
        Database.__init__(self)

        self.__objects = WeakValueDictionary()  #   OID -> SqlDatabaseObject

    ##########
    #   Database - Operations (general)
    def close(self) -> None:
        for (oid, obj) in self.__objects.items():
            obj._invalidate_property_cache()
            obj._mark_dead()
        Database.close(self)

    ##########
    #   Database - Operations (associations)
    def try_login(self, login: str, password: str) -> Optional[Account]:
        self._ensure_open() # may raise DatabaseError
        assert isinstance(login, str)
        assert isinstance(password, str)

        sha1 = hashlib.sha1()
        sha1.update(password.encode("utf-8"))
        password_hash = sha1.hexdigest().upper()

        stat = self.create_statement(
            """ SELECT [accounts].[pk] AS [account_oid]
                  FROM [users],[accounts]
                 WHERE [accounts].[fk_user] = [users].[pk]
                   AND [users].[enabled] = ?
                   AND [accounts].[enabled] = ?
                   AND [accounts].[login] = ?
                   AND [accounts].[password_hash] = ?""")
        stat.set_bool_parameter(0, True)
        stat.set_bool_parameter(1, True)
        stat.set_string_parameter(2, login)
        stat.set_string_parameter(3, password_hash)
        rs = stat.execute()
        assert len(rs) <= 1
        for r in rs:
            return self._get_account_proxy(r["account_oid"])
        return None

    @property
    def users(self) -> Set[User]:
        self._ensure_open() # may raise DatabaseError

        try:
            stat = self.create_statement(" SELECT [pk] FROM [users]")
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self._get_user_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def activity_types(self) -> Set[ActivityType]:
        self._ensure_open() # may raise DatabaseError

        try:
            stat = self.create_statement(" SELECT [pk] FROM [activity_types]")
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self._get_activity_type_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def public_activities(self) -> Set[PublicActivity]:
        self._ensure_open() # may raise DatabaseError

        try:
            stat = self.create_statement(" SELECT [pk] FROM [objects] WHERE [object_type_name] = ?")
            stat.set_string_parameter(0, Activity.TYPE_NAME)
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self._get_public_activity_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    @property
    def public_activities(self) -> Set[PublicActivity]:
        self._ensure_open() # may raise DatabaseError

        try:
            stat = self.create_statement(" SELECT [pk] FROM [public_activities]")
            rs = stat.execute()
            result = set()
            for r in rs:
                result.add(self._get_public_activity_proxy(r["pk"]))
            return result
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Overridables (database engine - specific)
    @property
    def string_opening_quote(self) -> str:
        return "'"  #   as per SQL standard

    @property
    def string_closing_quote(self) -> str:
        return "'"  #   as per SQL standard

    def quote_string_literal(self, s: str) -> str:
        assert isinstance(s, str)

        chunks = []
        scan = 0
        chunk = ""
        while scan < len(s):
            c = s[scan]
            if c == self.string_opening_quote:
                #   Quote must be reprsented as quote-quote within string literals
                chunk += self.string_opening_quote + self.string_opening_quote;
                scan += 1
            elif c == "\\":
                chunk += "\\\\"
                scan += 1
            elif ord(c) >= 32 and ord(c) < 127:
                chunk += c
                scan += 1
            else:   #   UNICODE, special characters
                chunks.append(self.string_opening_quote + chunk + self.string_closing_quote)
                chunk = ""
                chunks.append("CHAR(" + str(ord(c)) + ")")
                scan += 1
        #   Record the last chunk
        chunks.append(self.string_opening_quote + chunk + self.string_closing_quote)
        empty_literal = self.string_opening_quote + self.string_closing_quote
        chunks = list(filter(lambda x: x != empty_literal, chunks))
        return empty_literal if len(chunks) == 0 else "||".join(chunks)

    @property
    def identifier_opening_quote(self) -> str:
        return "\"" #   as per SQL standard

    @property
    def identifier_closing_quote(self) -> str:
        return "\"" #   as per SQL standard

    def quote_identifier(self, s: str) -> str:
        assert isinstance(s, str)
        return  self.identifier_opening_quote + s + self.identifier_closing_quote

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

    ##########
    #   Operations
    def execute_script(self, script: str) -> None:
        self._ensure_open() # may raise DatabaseError
        assert isinstance(script, str)

        #   First, we must break "script" into individual statements:
        #   *   Anything from -- to \n is a comment.
        #   *   Anything from /* to */ is a comment.
        #   *   Single quotes ', double quotes " and backticks ` all
        #       denote quoted identifiers/strings; comments within
        #       these are not recognized as well as other quote types.
        #   *   Statements are separated by ';'; empty statements
        #       are ignored.
        statements = []
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

    def create_statement(self, sql_template: str) -> SqlStatement:
        """
            Creates a new "SQL statement" that can be executed as
            necessary.

            @param sql_template:
                The SQL statement template.
            @raise DatabaseError:
                If an error occurs (e.g. invalid sql_template syntax, etc.)
        """
        self._ensure_open() # may raise DatabaseError
        assert isinstance(sql_template, str)

        sql_template = sql_template.strip()
        #   TODO cache SqlStatements on a per-thread basis for
        #   future reuse, keyed by sql_template

        #   TODO select, insert, delete, update require their own
        #   subclasses of SqlStatement!
        from .SqlInsertStatement import SqlInsertStatement
        from .SqlSelectStatement import SqlSelectStatement
        from .SqlUpdateStatement import SqlUpdateStatement
        from .SqlDeleteStatement import SqlDeleteStatement
        
        if sql_template.upper().startswith("INSERT"):
            sql_statement = SqlInsertStatement(self, sql_template)  #   may raise DatabaseError
        elif sql_template.upper().startswith("SELECT"):
            sql_statement = SqlSelectStatement(self, sql_template)  #   may raise DatabaseError
        elif sql_template.upper().startswith("UPDATE"):
            sql_statement = SqlUpdateStatement(self, sql_template)  #   may raise DatabaseError
        elif sql_template.upper().startswith("DELETE"):
            sql_statement = SqlDeleteStatement(self, sql_template)  #   may raise DatabaseError
        else:
            sql_statement = SqlStatement(self, sql_template)    #   may raise DatabaseError

        #   Done
        return sql_statement

    def format_parameter(self, type: type, value: Any) -> str:
        if value is None:
            return "NULL"
        try:
            if type is None:
                #   Auto-select formatting
                if isinstance(value, int):
                    return str(value)
                elif isinstance(value, float):
                    return str(value)
                elif isinstance(value, str):
                    return self.quote_string_literal(value)
                elif isinstance(value, bool):
                    return self.quote_string_literal("Y") if value else self.quote_string_literal("N")
                else:
                    raise NotImplementedError()
            else:
                #   Format to the required type
                match type:
                    case SqlDataType.INTEGER:
                        return str(int(value))
                    case SqlDataType.REAL:
                        return str(float(value))
                    case SqlDataType.STRING:
                        return self.quote_string_literal(value)
                    case SqlDataType.BOOLEAN:
                        return self.quote_string_literal("Y") if value else self.quote_string_literal("N")
                    case _:
                        raise NotImplementedError()
        except Exception as ex:
            raise DatabaseError.wrap(ex)

    ##########
    #   Database - Operations (life cycle)
    def create_user(self,
                    enabled: bool = True,
                    real_name: str = None,  #   MUST specify!
                    inactivity_timeout: Optional[int] = None,
                    ui_locale: Optional[Locale] = None,
                    email_addresses: List[str] = []) -> User:
        self._ensure_open() # may raise DatabaseError
        assert isinstance(enabled, bool)
        assert isinstance(real_name, str)
        assert (inactivity_timeout is None) or isinstance(inactivity_timeout, int)
        assert ui_locale is None or isinstance(ui_locale, Locale)
        assert isinstance(email_addresses, list)    #   and all elements are strings

        #   Validate parameters (real name is valid, etc.)
        validator = self.validator
        if not validator.user.is_valid_enabled(enabled):
            raise InvalidDatabaseObjectPropertyError(User.TYPE_NAME, User.ENABLED_PROPERTY_NAME, enabled)
        if not validator.user.is_valid_real_name(real_name):
            raise InvalidDatabaseObjectPropertyError(User.TYPE_NAME, User.REAL_NAME_PROPERTY_NAME, real_name)
        if not validator.user.is_valid_inactivity_timeout(inactivity_timeout):
            raise InvalidDatabaseObjectPropertyError(User.TYPE_NAME, User.INACTIVITY_TIMEOUT_PROPERTY_NAME, inactivity_timeout)
        if not validator.user.is_valid_ui_locale(ui_locale):
            raise InvalidDatabaseObjectPropertyError(User.TYPE_NAME, User.UI_LOCALE_PROPERTY_NAME, ui_locale)
        if not validator.user.is_valid_email_addresses(email_addresses):
            raise InvalidDatabaseObjectPropertyError(User.TYPE_NAME, User.EMAIL_ADDRESSES_PROPERTY_NAME, email_addresses)

        #   Make database changes
        try:
            self.begin_transaction();

            stat1 = self.create_statement(
                """INSERT INTO objects
                          (object_type_name)
                          VALUES (?)""");
            stat1.set_string_parameter(0, User.TYPE_NAME)
            user_oid = stat1.execute()

            stat2 = self.create_statement(
                """INSERT INTO users
                          (pk,enabled,real_name,inactivity_timeout,ui_locale,email_addresses)
                          VALUES (?,?,?,?,?,?)""");
            stat2.set_int_parameter(0, user_oid)
            stat2.set_bool_parameter(1, enabled)
            stat2.set_string_parameter(2, real_name)
            stat2.set_int_parameter(3, inactivity_timeout)
            stat2.set_string_parameter(4, None if ui_locale is None else repr(ui_locale))
            stat2.set_string_parameter(5, None if len(email_addresses) == 0 else "\n".join(email_addresses))
            stat2.execute()

            self.commit_transaction()
            user = self._get_user_proxy(user_oid)

            #   Issue notifications
            self.enqueue_notification(
                DatabaseObjectCreatedNotification(
                    self,
                    user))

            #   Done
            return user
        except Exception as ex:
            self.rollback_transaction()
            raise DatabaseError.wrap(ex)

    def create_activity_type(self,
                    name: str = None,
                    description: str = None) -> ActivityType:
        self._ensure_open() # may raise DatabaseError
        assert isinstance(name, str)
        assert isinstance(description, str)

        #   Validate parameters
        validator = self.validator
        if not validator.activity_type.is_valid_name(name):
            raise InvalidDatabaseObjectPropertyError(ActivityType.TYPE_NAME, ActivityType.NAME_PROPERTY_NAME, name)
        if not validator.activity_type.is_valid_description(description):
            raise InvalidDatabaseObjectPropertyError(ActivityType.TYPE_NAME, ActivityType.DESCRIPTION_PROPERTY_NAME, description)

        #   Make database changes
        try:
            self.begin_transaction();

            stat1 = self.create_statement(
                """INSERT INTO objects
                          (object_type_name)
                          VALUES (?)""");
            stat1.set_string_parameter(0, ActivityType.TYPE_NAME)
            activity_type_oid = stat1.execute()

            stat2 = self.create_statement(
                """INSERT INTO [activity_types]
                          ([pk],[name],[description])
                          VALUES (?,?,?)""");
            stat2.set_int_parameter(0, activity_type_oid)
            stat2.set_string_parameter(1, name)
            stat2.set_string_parameter(2, description)
            stat2.execute()

            self.commit_transaction()
            activity_type = self._get_activity_type_proxy(activity_type_oid)

            #   Issue notifications
            self.enqueue_notification(
                DatabaseObjectCreatedNotification(
                    self,
                    activity_type))

            #   Done
            return activity_type
        except Exception as ex:
            self.rollback_transaction()
            raise DatabaseError.wrap(ex)

    def create_public_activity(self,
                    name: str = None,           #   MUST specify!
                    description: str = None,    #   MUST specify!
                    activity_type: Optional[ActivityType] = None,
                    timeout: Optional[int] = None,
                    require_comment_on_start: bool = False,
                    require_comment_on_finish: bool = False,
                    full_screen_reminder: bool = False) -> PublicActivity:
        from .SqlActivityType import SqlActivityType

        self._ensure_open() # may raise DatabaseError
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert (activity_type is None) or isinstance(activity_type, SqlActivityType)
        assert (timeout is None) or isinstance(timeout, int)
        assert isinstance(require_comment_on_start, bool)
        assert isinstance(require_comment_on_finish, bool)
        assert isinstance(full_screen_reminder, bool)

        #   Validate parameters
        validator = self.validator
        if not validator.activity.is_valid_name(name):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.NAME_PROPERTY_NAME, name)
        if not validator.activity.is_valid_description(description):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.DESCRIPTION_PROPERTY_NAME, description)
        if not validator.activity.is_valid_timeout(timeout):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.TIMEOUT_PROPERTY_NAME, description)
        if not validator.activity.is_valid_require_comment_on_start(require_comment_on_start):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.TIMEOUT_PROPERTY_NAME, description)
        if not validator.activity.is_valid_require_comment_on_finish(require_comment_on_finish):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.TIMEOUT_PROPERTY_NAME, description)
        if not validator.activity.is_valid_full_screen_reminder(full_screen_reminder):
            raise InvalidDatabaseObjectPropertyError(PublicActivity.TYPE_NAME, PublicActivity.TIMEOUT_PROPERTY_NAME, description)
        if activity_type is not None:
            activity_type._ensure_live()
            if activity_type.database is not self:
                raise IncompatibleDatabaseObjectError(activity_type.type_name)

        #   Make database changes
        try:
            self.begin_transaction();

            stat1 = self.create_statement(
                """INSERT INTO [objects]
                          ([object_type_name])
                          VALUES (?)""");
            stat1.set_string_parameter(0, PublicActivity.TYPE_NAME)
            public_activity_oid = stat1.execute()

            stat2 = self.create_statement(
                """INSERT INTO [activities]
                          ([pk],[name],[description],[timeout],
                           [require_comment_on_start],[require_comment_on_finish],
                           [full_screen_reminder],[fk_activity_type])
                          VALUES (?,?,?,?,?,?,?,?)""");
            stat2.set_int_parameter(0, public_activity_oid)
            stat2.set_string_parameter(1, name)
            stat2.set_string_parameter(2, description)
            stat2.set_int_parameter(3, timeout)
            stat2.set_bool_parameter(4, require_comment_on_start)
            stat2.set_bool_parameter(5, require_comment_on_finish)
            stat2.set_bool_parameter(6, full_screen_reminder)
            stat2.set_int_parameter(7, None if activity_type is None else activity_type.oid)
            stat2.execute()

            stat3 = self.create_statement(
                """INSERT INTO [public_activities]
                          ([pk])
                          VALUES (?)""");
            stat3.set_int_parameter(0, public_activity_oid)
            stat3.execute()

            self.commit_transaction()
            public_activity = self._get_public_activity_proxy(public_activity_oid)

            #   Issue notifications
            self.enqueue_notification(
                DatabaseObjectCreatedNotification(
                    self,
                    public_activity))
            if activity_type is not None:
                self.enqueue_notification(
                    DatabaseObjectModifiedNotification(
                        self,
                        activity_type,
                        ActivityType.ACTIVITIES_ASSOCIATION_NAME))

            #   Done
            return public_activity
        except Exception as ex:
            self.rollback_transaction()
            raise DatabaseError.wrap(ex)

    ##########
    #   Implementation helpers (internal use only)
    def _ensure_open(self) -> None:
        if not self.is_open:
            raise DatabaseObjectDeadError("Database")

    def _get_user_proxy(self, oid: OID) -> User:
        from .SqlUser import SqlUser
        obj = self.__objects.get(oid, None)
        if isinstance(obj, SqlUser):
            return obj
        return SqlUser(self, oid)

    def _get_account_proxy(self, oid: OID) -> Account:
        from .SqlAccount import SqlAccount
        obj = self.__objects.get(oid, None)
        if isinstance(obj, SqlAccount):
            return obj
        return SqlAccount(self, oid)

    def _get_activity_type_proxy(self, oid: OID) -> User:
        from .SqlActivityType import SqlActivityType
        obj = self.__objects.get(oid, None)
        if isinstance(obj, SqlActivityType):
            return obj
        return SqlActivityType(self, oid)

    def _get_public_activity_proxy(self, oid: OID) -> User:
        from .SqlPublicActivity import SqlPublicActivity
        obj = self.__objects.get(oid, None)
        if isinstance(obj, SqlPublicActivity):
            return obj
        return SqlPublicActivity(self, oid)

    def _get_private_activity_proxy(self, oid: OID) -> User:
        from .SqlPrivateActivity import SqlPrivateActivity
        obj = self.__objects.get(oid, None)
        if isinstance(obj, SqlPrivateActivity):
            return obj
        return SqlPrivateActivity(self, oid)
