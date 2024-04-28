""" A persistent container where business data is kept,
    constituting of the underlying physical storage (database)
    and busibess/access rules . """

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from util.interface.api import *
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .WorkspaceType import WorkspaceType
from .WorkspaceAddress import WorkspaceAddress
from .Exceptions import WorkspaceError
from .Credentials import Credentials

##########
#   Public entities
@final
class WorkspaceMeta(ClassWithConstantsMeta):

    @property
    def current(cls) -> "Workspace":
        return Workspace._Workspace__current_workspace

    @current.setter
    def current(cls, value: "Workspace"):
        assert (value is None) or isinstance(value, Workspace)
        if value is not Workspace._Workspace__current_workspace:
            Workspace._Workspace__current_workspace = value
            #   TODO notify interested listeners of the "current workspace" change
            evt = PropertyChangeEvent(cls, cls, Workspace.CURRENT_WORKSPACE_PROPERTY_NAME)
            cls.process_property_change_event(evt)

@final
class Workspace(metaclass=WorkspaceMeta):
    """ A persistent container where business data is kept,
        constituting of the underlying physical storage (database)
        and busibess/access rules . """

    ##########
    #   Implementation
    __current_workspace = None
    __property_change_listeners = []

    ##########
    #   Constants (observable property names)
    CURRENT_WORKSPACE_PROPERTY_NAME = "current"
    """ The name of the "current: Workspace" static property of a Workspace. """

    ##########
    #   Construction (internal only)
    def __init__(self, address: WorkspaceAddress, db: Database):
        assert isinstance(address, WorkspaceAddress)
        assert isinstance(db, Database)

        self.__address = address
        self.__db = db

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
              credentials: Optional[Credentials] = None) -> Optional[Account]:
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

    ##########
    #   Operations (static property change handling)
    @staticmethod
    def add_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when a static property change event is
            processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l not in Workspace.__property_change_listeners:
            Workspace.__property_change_listeners.append(l)

    @staticmethod
    def remove_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a static property change
            event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l in Workspace.__property_change_listeners:
            Workspace.__property_change_listeners.remove(l)

    @staticproperty
    def property_change_listeners() -> list[Union[PropertyChangeEventListener, PropertyChangeEventHandler]]:
        """ The list of all static property change listeners registered so far. """
        return Workspace.__property_change_listeners.copy()

    @staticmethod
    def process_property_change_event(event : PropertyChangeEvent) -> bool:
        """
            Called to process an PropertyChangeEvent for a
            change made to a static property.

            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        for l in Workspace.property_change_listeners:
            try:
                if isinstance(l, PropertyChangeEventHandler):
                    l.on_property_change(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed

    ##########
    #   Implementation helpers
    def _get_business_proxy(self, data_object: DatabaseObject) -> "BusinessObject":
        raise NotImplementedError()
