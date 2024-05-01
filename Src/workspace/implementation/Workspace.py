""" A persistent container where business data is kept,
    constituting of the underlying physical storage (database)
    and busibess/access rules . """

#   Python standard library
from typing import final, Set
from weakref import WeakKeyDictionary, WeakValueDictionary
import threading

#   Dependencies on other PyTT components
from util.interface.api import *
import db.interface.api as dbapi

#   Internal dependencies on modules within the same component
from .WorkspaceType import WorkspaceType
from .WorkspaceAddress import WorkspaceAddress
from .Exceptions import WorkspaceError
from .Credentials import Credentials
from .Capabilities import Capabilities
from .BusinessObject import BusinessObject
from .BusinessUser import BusinessUser
from .Notifications import *

##########
#   Public entities
@final
class Workspace:
    """ A persistent container where business data is kept,
        constituting of the underlying physical storage (database)
        and busibess/access rules . """

    ##########
    #   Construction (internal only)
    def __init__(self, address: WorkspaceAddress, db: dbapi.Database):
        assert isinstance(address, WorkspaceAddress)
        assert isinstance(db, dbapi.Database)

        self.__address = address
        self.__db = db

        self.__lock = threading.RLock() #   for all access synchronization

        self.__map_data_objects_to_business_objects = WeakValueDictionary()
        self.__access_rights = WeakKeyDictionary()  #   Credentials -> Capabilities

        #   Forward database notifications to workspace clients
        self.__notification_listeners = []
        self.__notification_listeners_guard = threading.Lock()

        db.add_notification_listener(self.__on_database_notification)

    ##########
    #   Properties
    @property
    def type(self) -> WorkspaceType:
        """ The type of this workspace; can be safely obtained
            for both open and closed woorkspaces. """
        return self.__address.workspace_type

    @property
    def address(self) -> WorkspaceAddress:
        """ The address of this workspace; can be safely obtained
            for both open and closed workspaces. """
        return self.__address

    @abstractproperty
    def is_open(self) -> bool:
        """ True if this Workspace is currently open (i.e. can be
            used to access the physical database), False if closed. """
        return self.__db.is_open

    @property
    def lock(self) -> threading.RLock:
        """ The RLock object to use for all threaded access synchronization. """
        return self.__lock

    ##########
    #   Operations (general)
    def close(self) -> None:
        """
            Closes this Workspace; has no effect if already closed.

            @raise WorkspaceError:
                If an error occurs; the Workspace object is
                still "closed" before the exception is thrown.
        """
        try:
            self.__db.close()
        except Exception as ex:
            raise WorkspaceError(str(ex)) from ex

    ##########
    #   Operations (access control)
    def get_capabilities(self, credentials: Credentials) -> Capabilities:
        """
            Returns the Capabilities granted by the specified
            user credentials.

            @param credentials:
                The user credentials.
            @return:
                The Capabilities granted by the specified user
                credentials, can be Capabilities.NONE if the
                specfied credentials are e.g. not in the database.
            @raise WorkspaceError:
                If a data access error occurs.
        """
        self._ensure_open() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        capabilities = self.__access_rights.get(credentials, None)
        if capabilities is None:
            try:
                data_account = self.__db.try_login(credentials.login, credentials._Credentials__password)
                if (data_account is not None) and data_account.enabled and data_account.user.enabled:
                    capabilities = data_account.capabilities
                else:
                    capabilities = Capabilities.NONE
                self.__access_rights[credentials] = capabilities
            except Exception as ex:
                raise WorkspaceError.wrap(ex)
        return capabilities

    def can_manage_users(self, credentials: Credentials) -> bool:
        self._ensure_open() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)

        capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
        if capabilities is None:
            return False
        return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_USERS)

    ##########
    #   Operations (associations)
    def try_login(self, login: Optional[str], password: Optional[str],
                  credentials: Optional[Credentials]) -> Optional["BusinessAccount"]:
        """
            Attempts a login. If the account with the specified
            login and password exists in this database, is enabled
            and belongs to an enabled user, then returns it; else
            returns None.

            @param login:
                The account login.
            @param password:
                The account password.
            @raise DatabaseError:
                If an error occurs.
        """
        try:
            args = locals()
            if isinstance(login, str) and isinstance(password, str):
                data_account = self.__db.try_login(login, password)
            elif isinstance(credentials, Credentials):
                data_account = self.__db.try_login(credentials.login, credentials._Credentials__password)
            else:
                raise WorkspaceError("Invalod login parameters " + str(args))
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
        return self._get_business_proxy(data_account)

    def login(self, login: Optional[str] = None, password: Optional[str] = None,
              credentials: Optional[Credentials] = None) -> Optional["BusinessAccount"]:
        """
            Performs a login. If the account with the specified
            login and password exists in this database, is enabled
            and belongs to an enabled user, then returns it; else
            an error occurs.

            Either login+password or credentials must be specified.

            @param login:
                The account login.
            @param password:
                The account password.
            @param credentials:
                The credentials to use for login.
            @raise DatabaseError:
                If an error occurs.
        """
        try:
            args = locals()
            if isinstance(login, str) and isinstance(password, str):
                data_account = self.__db.login(login, password)
            elif isinstance(credentials, Credentials):
                data_account = self.__db.login(credentials.login, credentials._Credentials__password)
            else:
                raise WorkspaceError("Invalod login parameters " + str(args))
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
        return self._get_business_proxy(data_account)

    def get_users(self, credentials: Credentials) -> Set[BusinessUser]:
        assert isinstance(credentials, Credentials)

        try:
            result = set()
            if self.get_capabilities(credentials) is None:
                #   The caller has no access to the database OR account/user is disables
                pass
            elif self.can_manage_users(credentials):
                #   The caller can see all users
                for data_user in self.__db.users:
                    result.add(self._get_business_proxy(data_user))
            else:
                #   The caller can only see their own user
                data_account = self.__db.login(credentials.login, credentials.__password)
                result.add(self._get_business_proxy(data_account.user))
            return result
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (notifications)
    def add_notification_listener(self, l: Union[WorkspaceNotificationListener, WorkspaceNotificationHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when a workspace notification is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect.

            IMPORTANT: This method is thread-safe."""
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WorkspaceNotificationHandler))
        with self.__notification_listeners_guard:
            if l not in self.__notification_listeners:
                self.__notification_listeners.append(l)

    def remove_notification_listener(self, l: Union[WorkspaceNotificationListener, WorkspaceNotificationHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a workspace notification is
            processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect.

            IMPORTANT: This method is thread-safe."""
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, WorkspaceNotificationHandler))
        with self.__notification_listeners_guard:
            if l in self.__notification_listeners:
                self.__notification_listeners.remove(l)

    @property
    def notification_listeners(self) -> list[Union[WorkspaceNotificationListener, WorkspaceNotificationHandler]]:
        """ The list of all notification listeners registered so far.

            IMPORTANT: This property is thread-safe. """
        with self.__notification_listeners_guard:
            return self.__notification_listeners.copy()

    def process_notification(self, n: WorkspaceNotification) -> bool:
        """
            Called to process a WorkspaceNotification.
            IMPORTANT: The hidden notification thread running behind
            a Workspace will call this method when notifications are
            enqueued and must then be processed.

            IMPORTANT: This method is thread-safe.

            @param self:
                The workspace on which the method has been called.
            @param event:
                The notification to process.
        """
        assert isinstance(n, WorkspaceNotification)
        for l in self.notification_listeners:
            try:
                if isinstance(l, WorkspaceNotificationHandler):
                    if isinstance(n, BusinessObjectCreatedNotification):
                        l.on_workspace_object_created(n)
                    elif isinstance(n, BusinessObjectDestroyedNotification):
                        l.on_workspace_object_destroyed(n)
                    elif isinstance(n, BusinessObjectModifiedNotification):
                        l.on_workspace_object_modified(n)
                    else:
                        raise NotImplementedError()
                    l.on_property_change(n)
                else:
                    l(n)
            except Exception as ex:
                pass    #   TODO log the exception

    ##########
    #   Implementation helpers
    def _ensure_open(self) -> None:
        if not self.__db.is_open:
            raise WorkspaceObjectDeadError("Workspace")

    def _get_business_proxy(self, data_object: dbapi.DatabaseObject) -> BusinessObject:
        from .BusinessUser import BusinessUser
        from .BusinessAccount import BusinessAccount

        assert isinstance(data_object, dbapi.DatabaseObject)
        business_object = self.__map_data_objects_to_business_objects.get(data_object, None)
        if business_object is None:
            #   Need to create a new business proxy for the data_object
            if isinstance(data_object, dbapi.User):
                business_object = BusinessUser(self, data_object)
            elif isinstance(data_object, dbapi.Account):
                business_object = BusinessAccount(self, data_object)
            else:
                raise NotImplementedError()
            self.__map_data_objects_to_business_objects[data_object] = business_object
        else:
            #   Business proxy already exists - make sure it's valid
            assert business_object._data_object is data_object
        return business_object

    ##########
    #   Event handlers
    def __on_database_notification(self, dbn: dbapi.DatabaseNotification) -> None:
        #TODO kill off print(str(threading.current_thread().ident) + ":" + repr(dbn))
        #   This listener is called on the notification thread
        #   internal to the underlying Database. Normally we would
        #   just forward notifications to the Workspace clients; however,
        #   some DB notifications must cause e.g. invalidation of the
        #   Workspace caches, etc.
        if (isinstance(dbn, dbapi.DatabaseObjectCreatedNotification) or
            isinstance(dbn, dbapi.DatabaseObjectDestroyedNotification) or
            isinstance(dbn, dbapi.DatabaseObjectModifiedNotification)):
            #   If User or Account is affected in any way, we may have
            #   to recalculate all cached access rights
            if isinstance(dbn.object, dbapi.User) or isinstance(dbn.object, dbapi.Account):
                with self.__lock:
                    self.__access_rights.clear()
        #   ...and now to the forwarding
        if isinstance(dbn, dbapi.DatabaseObjectCreatedNotification):
            n = BusinessObjectCreatedNotification(self, self._get_business_proxy(dbn.object))
        elif isinstance(dbn, dbapi.DatabaseObjectDestroyedNotification):
            n = BusinessObjectDestroyedNotification(self, self._get_business_proxy(dbn.object))
        elif isinstance(dbn, dbapi.DatabaseObjectModifiedNotification):
            n = BusinessObjectModifiedNotification(self, self._get_business_proxy(dbn.object), dbn.property_name)
        else:
            raise NotImplementedError()
        self.process_notification(n)
