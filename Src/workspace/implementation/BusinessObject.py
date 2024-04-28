""" A common base class for all objects residing in a workspace. """
#   Python standard library
from abc import abstractmethod
from typing import TypeAlias

#   Dependencies on other PyTT components
from db.interface.api import DatabaseObject, OID as DbOID
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
from .Capabilities import Capabilities
from .Exceptions import *

##########
#   Public entities
OID: TypeAlias = DbOID

class BusinessObject(ABCWithConstants):
    """ A common base class for all objects residing in a workspace. """

    ##########
    #   Construction
    def __init__(self, workspace: "Workspace", data_object: DatabaseObject):
        from .Workspace import Workspace
        assert isinstnce(workspace, Workspace)
        assert isinstnce(data_object, DatabaseObject)
        
        self.__workspace = workspace
        self.__data_object = data_object

    ##########
    #   object
    def __str__(self) -> str:
        return self.__data_object.type_display_name + ' ' + self.__data_object.display_name

    ##########
    #   UI traits
    @property
    def display_name(self) -> str:
        """ The user-readable display name of this business object. """
        return self.__data_object.display_name

    @property
    def type_name(self) -> str:
        """ The internal name of this business object's type (e.g. "User",
            "PublicTask", etc.) """
        return self.__data_object.type_name

    @property
    def type_display_name(self) -> str:
        """ The user-readable display name of this business object's type
            (e.g. "user", "public task", etc.) """
        return self.__data_object.type_display_name

    @property
    def small_image(self) -> tk.PhotoImage:
        """ The small (16x16) image representing this datbase object. """
        return self.__data_object.small_image

    @property
    def large_image(self) -> tk.PhotoImage:
        """ The large (32x32) image representing this datbase object. """
        return self.__data_object.large_image

    ##########
    #   Properties
    @property
    def workspace(self) -> "Workspace":
        """ The workspace to which this object belongs if live) or 
            used to belong (if dead). """
        return self.__workspace

    @property
    def live(self) -> bool:
        """ True of this workspace object [proxy] is live, false if dead. """
        return self.__data_object.live

    @property
    def oid(self) -> OID:
        """ The OID of this object (if live) or the OID this object
            used to have (if dead). """
        return self.__data_object.oid

    ##########
    #   Operations (access control)
    @abstractmethod
    def can_destroy(self, credentials: Credentials) -> bool:
        """
            Checks whether the specified credentials allow 
            destroying this business object.
            
            @param credentials:
                The credentials to check.
            @return:
                True if the specified credentials allow destroying 
                this business object, False if not.
            @raise WorkspaceError:
                If a data access error occurs.
        """
        raise NotImplementedError()
    
    ##########
    #   Operations (life cycle)
    def destroy(self, credentials: Credentials) -> None:
        """
            Destroys this object, delete-cascading as necessary.

            @param credentials:
                The credentials of the service caller.
            @raise WorkspaceError:
                If an error occurs.
        """
        self._ensure_live() # may raise WorkspaceError
        assert isinstance(credentials, Credentials)
        
        if not self.can_destroy(credentials):
            raise AccessDeniedError()
        try:
            self.__data_object.destroy()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
    
    ##########
    #   Implementation helpers
    def _ensure_live(self) -> None:
        self.__workspace._ensure_open() # may raise WorkspaceError
        try:
            self.__data_object._ensure_live()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

