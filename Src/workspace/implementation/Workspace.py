""" A persistent container where business data is kept,
    constituting of the underlying physical storage (database)
    and busibess/access rules . """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import final, Set, List
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
from .BusinessActivityType import BusinessActivityType
from .BusinessPublicActivity import BusinessPublicActivity
from .BusinessPrivateActivity import BusinessPrivateActivity
from .BusinessPublicTask import BusinessPublicTask
#   TODO from .BusinessPrivateTask import BusinessPrivateTask
from .Notifications import *
from .Validator import *

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
    #   object (entry/exit protocol needed for Dialog.do_modal
    def __enter__(self) -> None:
        self.__lock.acquire()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.__lock.release()

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

    @property
    def is_open(self) -> bool:
        """ True if this Workspace is currently open (i.e. can be
            used to access the physical database), False if closed. """
        return self.__db.is_open

    @property
    def validator(self) -> Validator:
        """ The Validator used by this Workspace. """
        return self.__db.validator

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
        with self:
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
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_USERS)

    def can_manage_stock_items(self, credentials: Credentials) -> bool:
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_STOCK_ITEMS)

    def can_manage_public_activities(self, credentials: Credentials) -> bool:
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_PUBLIC_ACTIVITIES)

    def can_manage_private_activities(self, credentials: Credentials) -> bool:
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_PRIVATE_ACTIVITIES)

    def can_manage_public_tasks(self, credentials: Credentials) -> bool:
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_PUBLIC_TASKS)

    def can_manage_private_tasks(self, credentials: Credentials) -> bool:
        with self:
            self._ensure_open() # may raise WorkspaceError
            assert isinstance(credentials, Credentials)

            capabilities = self.get_capabilities(credentials)   # may raise WorkspaceError
            if capabilities is None:
                return False
            return capabilities.contains_any(Capabilities.ADMINISTRATOR, Capabilities.MANAGE_PRIVATE_TASKS)

    ##########
    #   Operations (associations)
    def try_login(self, login: Optional[str], password: Optional[str],
                  credentials: Optional[Credentials]) -> Optional[BusinessAccount]:
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
        with self:
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
              credentials: Optional[Credentials] = None) -> Optional[BusinessAccount]:
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
        with self:
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

        with self:
            try:
                result = set()
                if self.get_capabilities(credentials) is None:
                    #   The caller has no access to the database OR account/user is disabled
                    pass
                elif (self.can_manage_users(credentials) or 
                      self.can_manage_private_activities(credentials) or
                      self.can_manage_private_tasks(credentials)):
                    #   The caller can see all users.
                    #   Note that when the "credentials" allow managing private
                    #   activities or tasks of any user, the caller must be able
                    #   to SEE these other users so as to manage their private
                    #   activities and/or tasks
                    for data_user in self.__db.users:
                        result.add(self._get_business_proxy(data_user))
                else:
                    #   The caller can only see their own user
                    data_account = self.__db.login(credentials.login, credentials._Credentials__password)
                    result.add(self._get_business_proxy(data_account.user))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def get_activity_types(self, credentials: Credentials) -> Set[BusinessActivityType]:
        assert isinstance(credentials, Credentials)

        with self:
            try:
                result = set()
                if self.get_capabilities(credentials) is not None:
                    #   The caller can see all activity types
                    for data_activity_type in self.__db.activity_types:
                        result.add(self._get_business_proxy(data_activity_type))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def get_public_activities(self, credentials: Credentials) -> Set[BusinessActivityType]:
        assert isinstance(credentials, Credentials)

        with self:
            try:
                result = set()
                if self.get_capabilities(credentials) is not None:
                    #   The caller can see all public activities
                    for public_activity in self.__db.public_activities:
                        result.add(self._get_business_proxy(public_activity))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def get_all_public_tasks(self, credentials: Credentials) -> Set[BusinessPublicTask]:
        """
            Returns the unordered set of all BusinessPublicTasks in this 
            Workspace, whether root, leaf or intermediate.
            
            @return:
                The unordered set of all BusinessPublicTasks in this 
                Workspace, whether root, leaf or intermediate.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)

        with self:
            try:
                result = set()
                if self.get_capabilities(credentials) is not None:
                    #   The caller can see all public tasks
                    for public_task in self.__db.all_public_tasks:
                        result.add(self._get_business_proxy(public_task))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def get_root_public_tasks(self, credentials: Credentials) -> Set[BusinessPublicTask]:
        """
            Returns the unordered set of all root BusinessPublicTasks in 
            this Workspace.

            @return:
                The unordered set of all root BusinessPublicTasks in 
                this Workspace.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)

        with self:
            try:
                result = set()
                if self.get_capabilities(credentials) is not None:
                    #   The caller can see all public tasks
                    for public_task in self.__db.root_public_tasks:
                        result.add(self._get_business_proxy(public_task))
                return result
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    ##########
    #   Operations (life cycle)
    def create_user(self,
                    credentials: Credentials,
                    enabled: bool = True,
                    real_name: str = None,  #   MUST specify!
                    inactivity_timeout: Optional[int] = None,
                    ui_locale: Optional[Locale] = None,
                    email_addresses: List[str] = []) -> BusinessUser:
        """
            Creates a new BusinessUser.

            @param credentials:
                The credentials of the service caller.
            @param enabled:
                True to create an initially enabled BusinessUser, False
                to create an initially disabled BusinessUser.
            @param real_name:
                The "real name" for the new BusinessUser.
            @param inactivity_timeout:
                The inactivity timeout for the new BusinessUser, expressed
                in minutes, or None if the new user shall have no
                inactivity timeout.
            @param ui_locale:
                The preferred UI locale for the new BusinessUser, or None if
                the new user shall have no preferred UI locale (and will
                be therefore using the system/default UI Locale).
            @param email_addresses:
                The list of e-mail addresses for the new BusinessUser;
                cannot be None or contain Nones, but can be empty.
            @return:
                The newly created BusinessUser.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)
        assert isinstance(enabled, bool)
        assert isinstance(real_name, str)
        assert (inactivity_timeout is None) or isinstance(inactivity_timeout, int)
        assert (ui_locale is None) or isinstance(ui_locale, Locale)
        assert isinstance(email_addresses, list)
        assert all(isinstance(a, str) for a in email_addresses)

        with self:
            self._ensure_open()
            try:
                if not self.can_manage_users(credentials):
                    raise WorkspaceAccessDeniedError()
                data_user = self.__db.create_user(
                    enabled=enabled,
                    real_name=real_name,
                    inactivity_timeout=inactivity_timeout,
                    ui_locale=ui_locale,
                    email_addresses=email_addresses)
                return self._get_business_proxy(data_user)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def create_activity_type(self,
                             credentials: Credentials,
                             name: str = None,
                             description: str = None) -> BusinessActivityType:
        """
            Creates a new BusinessActivityType.

            @param credentials:
                The credentials of the service caller.
            @param name:
                The "name" for the new ActivityType.
            @param description:
                The "description" for the new ActivityType.
            @return:
                The newly created ActivityType.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(credentials, Credentials)
        assert isinstance(name, str)
        assert isinstance(description, str)

        with self:
            self._ensure_open()
            try:
                if not self.can_manage_stock_items(credentials):
                    raise WorkspaceAccessDeniedError()
                data_activity_type = self.__db.create_activity_type(
                    name=name,
                    description=description)
                return self._get_business_proxy(data_activity_type)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def create_public_activity(self,
                               credentials: Credentials,
                               name: str = None,           #   MUST specify!
                               description: str = None,    #   MUST specify!
                               activity_type: Optional[BusinessActivityType] = None,
                               timeout: Optional[int] = None,
                               require_comment_on_start: bool = False,
                               require_comment_on_finish: bool = False,
                               full_screen_reminder: bool = False) -> BusinessPublicActivity:
        assert isinstance(credentials, Credentials)
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert (activity_type is None) or isinstance(activity_type, BusinessActivityType)
        assert (timeout is None) or isinstance(timeout, int)
        assert isinstance(require_comment_on_start, bool)
        assert isinstance(require_comment_on_finish, bool)
        assert isinstance(full_screen_reminder, bool)

        with self:
            self._ensure_open() # may raise DatabaseError
            try:
                #   Validate parameters
                if activity_type is not None:
                    activity_type._ensure_live()
                    if activity_type.workspace is not self:
                        raise IncompatibleWorkspaceObjectError(activity_type.type_name)
                #   Validate access rights
                if not self.can_manage_public_activities(credentials):
                    raise WorkspaceAccessDeniedError()
                #   The rest of the work is up to the DB
                data_public_activity = self.__db.create_public_activity(
                    name=name,
                    description=description,
                    activity_type=None if activity_type is None else activity_type._data_object,
                    timeout=timeout,
                    require_comment_on_start=require_comment_on_start,
                    require_comment_on_finish=require_comment_on_finish,
                    full_screen_reminder=full_screen_reminder)
                return self._get_business_proxy(data_public_activity)
            except Exception as ex:
                raise WorkspaceError.wrap(ex)

    def create_public_task(self,
                           credentials: Credentials,
                           name: str = None,           #   MUST specify!
                           description: str = None,    #   MUST specify!
                           activity_type: Optional[BusinessActivityType] = None,
                           timeout: Optional[int] = None,
                           require_comment_on_start: bool = False,
                           require_comment_on_finish: bool = False,
                           full_screen_reminder: bool = False,
                           completed: bool = False) -> BusinessPublicTask:
        """
            Creates a new root BusinessPublicTask.

            @param name:
                The "name" for the new BusinessPublicTask.
            @param description:
                The "description" for the new BusinessPublicTask.
            @param activity_type:
                The activity type to assign to this BusinessPublicTask or None.
            @param timeout:
                The timeout of this BusinessPublicTask, expressed in minutes, or None.
            @param require_comment_on_start:
                True if user shall be required to enter a comment 
                when starting this BusinessPublicTask, else False.
            @param require_comment_on_finish:
                True if user shall be required to enter a comment 
                when finishing this BusinessPublicTask, else False.
            @param full_screen_reminder:
                True if user shall be shown a full-screen reminder 
                while this BusinessPublicTask is underway, else False.
            @param completed:
                True if the newly created BusinessPublicTask shall initially 
                be marked as "completed", False if not.
            @return:
                The newly created BusinessPublicTask.
            @raise WorkspaceError:
                If an error occurs.
        """
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert (activity_type is None) or isinstance(activity_type, BusinessActivityType)
        assert (timeout is None) or isinstance(timeout, int)
        assert isinstance(require_comment_on_start, bool)
        assert isinstance(require_comment_on_finish, bool)
        assert isinstance(full_screen_reminder, bool)
        assert isinstance(completed, bool)    

        with self:
            self._ensure_open() # may raise DatabaseError
            try:
                #   Validate parameters
                if activity_type is not None:
                    activity_type._ensure_live()
                    if activity_type.workspace is not self:
                        raise IncompatibleWorkspaceObjectError(activity_type.type_name)
                #   Validate access rights
                if not self.can_manage_public_tasks(credentials):
                    raise WorkspaceAccessDeniedError()
                #   The rest of the work is up to the DB
                data_public_task = self.__db.create_public_task(
                    name=name,
                    description=description,
                    activity_type=None if activity_type is None else activity_type._data_object,
                    timeout=timeout,
                    require_comment_on_start=require_comment_on_start,
                    require_comment_on_finish=require_comment_on_finish,
                    full_screen_reminder=full_screen_reminder,
                    completed=completed)
                return self._get_business_proxy(data_public_task)
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
        from .BusinessActivityType import BusinessActivityType

        assert isinstance(data_object, dbapi.DatabaseObject)
        business_object = self.__map_data_objects_to_business_objects.get(data_object, None)
        if business_object is None:
            #   Need to create a new business proxy for the data_object
            if isinstance(data_object, dbapi.User):
                business_object = BusinessUser(self, data_object)
            elif isinstance(data_object, dbapi.Account):
                business_object = BusinessAccount(self, data_object)
            elif isinstance(data_object, dbapi.ActivityType):
                business_object = BusinessActivityType(self, data_object)
            elif isinstance(data_object, dbapi.PublicTask):
                business_object = BusinessPublicTask(self, data_object)
            elif isinstance(data_object, dbapi.PrivateTask):
                business_object = BusinessPrivateTask(self, data_object)
            elif isinstance(data_object, dbapi.PublicActivity):
                business_object = BusinessPublicActivity(self, data_object)
            elif isinstance(data_object, dbapi.PrivateActivity):
                business_object = BusinessPrivateActivity(self, data_object)
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
