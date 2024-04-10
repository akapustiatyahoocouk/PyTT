#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .WorkspaceType import WorkspaceType
from .WorkspaceAddress import WorkspaceAddress
from .Exceptions import WorkspaceError

##########
#   Public entities
@final
class WorkspaceMeta(type, PropertyChangeEventProcessorMixin):
    
    @property
    def current(cls) -> "Workspace":
        return Workspace._Workspace__current
        
    @current.setter
    def current(cls, value: "Workspace"):
        assert (value is None) or isinstance(value, Workspace)
        if value is not Workspace._Workspace__current:
            Workspace._Workspace__current = value
            #   TODO notify interested listeners of the "current workspace" change
            evt = PropertyChangeEvent(cls, cls, Workspace.CURRENT_WORKSPACE_PROPERTY_NAME)
            cls.process_property_change_event(evt)

@final
class Workspace(metaclass=WorkspaceMeta):

    ##########
    #   Constants (observable property names)
    CURRENT_WORKSPACE_PROPERTY_NAME = "current"
    """ The name of the "current: Workspace" static property of a Workspace. """

    ######
    #   Implementation    
    __current = None
    
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
    def workspace_type(self) -> WorkspaceType:
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
