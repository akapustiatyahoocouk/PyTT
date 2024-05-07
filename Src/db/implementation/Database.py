""" A persistent container where data is kept. """

#   Python standard library
from typing import List, Union
from abc import ABC, abstractmethod, abstractproperty
from threading import Lock, Semaphore
from queue import Empty, Queue

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .DatabaseAddress import DatabaseAddress
from .DatabaseType import DatabaseType
from .Exceptions import DatabaseAccessDeniedError
from .Notifications import *
from .Validator import *

##########
#   Public entities
class Database(ABC):
    """ A persistent container where data is kept. """

    ##########
    #   Construction
    def __init__(self):

        self.__queued_notifications = Queue()

        #   TODO make list elements WEAK references to actual listeners
        self.__notification_listeners = []
        self.__notification_listeners_guard = Lock()

        self.__notification_thread_stop_requested = False
        self.__notification_thread = Thread(target=self.__run_notification_thread, args=[])
        self.__notification_thread.daemon = True
        self.__notification_thread.start()

    ##########
    #   object (entry/exit protocol needed for Dialog.do_modal
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        try:
            self.close()
        except:
            pass    #   TODO log

    ##########
    #   Properties
    @abstractproperty
    def type(self) -> DatabaseType:
        """ The type of this database; can be safely obtained
            for both open and closed databases. """
        raise NotImplementedError()

    @abstractproperty
    def address(self) -> DatabaseAddress:
        """ The address of this database; can be safely obtained
            for both open and closed databases. """
        raise NotImplementedError()

    @abstractproperty
    def is_open(self) -> bool:
        """ True if this Database is currently open (i.e. can be
            used to access the physical database), False if closed. """
        raise NotImplementedError()

    @abstractproperty
    def validator(self) -> Validator:
        """ The Validator used by this database. """
        raise NotImplementedError()

    ##########
    #   Operations (general)
    @abstractmethod
    def close(self) -> None:
        """
            Closes this Database; has no effect if already closed.

            @raise DatabaseError:
                If an error occurs; the Database object is
                still "closed" before the exception is thrown.
        """
        self.__notification_thread_stop_requested = True # stops notification thread eventually

    ##########
    #   Operations (associations)
    @abstractmethod
    def try_login(self, login: str, password: str) -> Optional["Account"]:
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
        raise NotImplementedError()

    def login(self, login: str, password: str) -> Optional["Account"]:
        """
            Performs a login. If the account with the specified
            login and password exists in this database, is enabled
            and belongs to an enabled user, then returns it; else
            an error occurs.

            @param login:
                The account login.
            @param password:
                The account password.
            @raise DatabaseError:
                If an error occurs.
        """
        assert isinstance(login, str)
        assert isinstance(password, str)

        account = self.try_login(login, password)
        if account is None:
            raise DatabaseAccessDeniedError()
        return account

    @abstractproperty
    def users(self) -> Set["User"]:
        """
            The unordered set of all Users in this Database.
            
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()
            
    @abstractproperty
    def activity_types(self) -> Set["ActivityType"]:
        """
            The unordered set of all ActivityTypes in this Database.
            
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Operations (life cycle)
    @abstractmethod
    def create_user(self,
                    enabled: bool = True,
                    real_name: str = None,  #   MUST specify!
                    inactivity_timeout: Optional[int] = None,
                    ui_locale: Optional[Locale] = None,
                    email_addresses: List[str] = []) -> "User":
        """
            Creates a new User.

            @param enabled:
                True to create an initially enabled User, False
                to create an initially disabled User.
            @param real_name:
                The "real name" for the new User.
            @param inactivity_timeout:
                The inactivity timeout for the new User, expressed
                in minutes, or None if the new user shall have no
                inactivity timeout.
            @param ui_locale:
                The preferred UI locale for the new User, or None if
                the new user shall have no preferred UI locale (and will
                be therefore using the system/default UI Locale).
            @param email_addresses:
                The list of e-mail addresses for the new User;
                cannot be None or contain Nones, but can be empty.
            @return:
                The newly created User.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_activity_type(self,
                    name: str = None,       #   MUST specify!
                    description: str = None) -> "ActivityType":
        """
            Creates a new ActivityType.

            @param name:
                The "name" for the new ActivityType.
            @param description:
                The "description" for the new ActivityType.
            @return:
                The newly created ActivityType.
            @raise DatabaseError:
                If an error occurs.
        """
        raise NotImplementedError()

    ##########
    #   Operations (notifications)
    def add_notification_listener(self, l: Union[DatabaseNotificationListener, DatabaseNotificationHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when adatabase notification is processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect.

            IMPORTANT: This method is thread-safe."""
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, DatabaseNotificationHandler))
        with self.__notification_listeners_guard:
            if l not in self.__notification_listeners:
                self.__notification_listeners.append(l)

    def remove_notification_listener(self, l: Union[DatabaseNotificationListener, DatabaseNotificationHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a database notification is
            processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect.

            IMPORTANT: This method is thread-safe."""
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, DatabaseNotificationHandler))
        with self.__notification_listeners_guard:
            if l in self.__notification_listeners:
                self.__notification_listeners.remove(l)

    @property
    def notification_listeners(self) -> list[Union[DatabaseNotificationListener, DatabaseNotificationHandler]]:
        """ The list of all notification listeners registered so far.

            IMPORTANT: This property is thread-safe. """
        with self.__notification_listeners_guard:
            return self.__notification_listeners.copy()

    def process_notification(self, n: DatabaseNotification) -> bool:
        """
            Called to process a DatabaseNotification.
            IMPORTANT: The hidden notification thread running behind
            a Database will call this method when notifications are
            enqueued and must then be processed.

            IMPORTANT: This method is thread-safe.

            @param self:
                The Database on which the method has been called.
            @param event:
                The notification to process.
        """
        assert isinstance(n, DatabaseNotification)
        for l in self.notification_listeners:
            try:
                if isinstance(l, DatabaseNotificationHandler):
                    if isinstance(n, DatabaseObjectCreatedNotification):
                        l.on_database_object_created(n)
                    elif isinstance(n, DatabaseObjectDestroyedNotification):
                        l.on_database_object_destroyed(n)
                    elif isinstance(n, DatabaseObjectModifiedNotification):
                        l.on_database_object_modified(n)
                    else:
                        raise NotImplementedError()
                    l.on_property_change(n)
                else:
                    l(n)
            except Exception as ex:
                pass    #   TODO log the exception

    def enqueue_notification(self, n: DatabaseNotification) -> None:
        """
            Enqueues a DatabaseNotification to be processed as 
            soon as practicable by the hidden notification thread.

            IMPORTANT: This method is thread-safe.
            
            @param n:
                The notification to enqueue.
        """
        assert isinstance(n, DatabaseNotification)
        self.__queued_notifications.put(n)

    ##########
    #   Threads
    def __run_notification_thread(self) -> None:
        while not self.__notification_thread_stop_requested:
            try:
                n = self.__queued_notifications.get(block=True, timeout=1)  # wait in 1s chunks
                assert isinstance(n, DatabaseNotification)
                self.process_notification(n)
            except Empty:   #   queue is still empty after a wait chunk
                pass