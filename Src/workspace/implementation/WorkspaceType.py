"""
    Defines the "Workspace type" ADT.
"""
#   Python standard library
from typing import final, Set

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .Exceptions import WorkspaceError

##########
#   Public entities
@final
class WorkspaceType:
    
    ##########
    #   Implementation
    __all = None

    ##########
    #   Construction (internal only)
    def __init__(self, db_type: DatabaseType):
        assert isinstance(db_type, DatabaseType)

        self.__db_type = db_type

    ##########
    #   object
    def __str__(self) -> str:
        return str(self.__db_type)

    ##########
    #   Properties
    @staticproperty
    def all() -> Set["WorkspaceType"]:
        if WorkspaceType.__all is None:
            WorkspaceType.__all = list()
            for db_type in DatabaseType.all:
                WorkspaceType.__all.append(WorkspaceType(db_type))
        return WorkspaceType.__all

    ##########
    #   Properties (general)
    @property
    def mnemonic(self) -> str:
        """ The mnemonic identifier of this workspace type. """
        return self.__db_type.mnemonic

    @property
    def display_name(self) -> str:
        """ The user-readable display name of this workspace type. """
        return self.__db_type.display_name

    ##########
    #   Workspace address handling
    def parse_workspace_address(self, external_form: str) -> "WorkspaceAddress":
        """
            Parses an external (re-parsable) form of a workspace address
            of this type.
            
            @param external_form:
                The external (re-parsable) form of a workspace address.
            @return:
                The parsed workspace address.
            @raise WorkspaceException:
                If the specified external form of a workspace address
                does not make sense for this workspace type.
        """
        try:
            dba = self.__db_type.parse_database_address(external_form)
            raise NotImplementedError()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    @property
    def default_workspace_address(self) -> "WorkspaceAddress":
        """ The address of the "default" workspace of this type;
            None if this workspace type has no concept of and
            "default" workspace. """
        raise NotImplementedError()

    def enter_new_workspace_address(self, parent: tk.BaseWidget) -> "WorkspaceAddress":
        """
            Prompts the user to interactively specify an address
            for a new workspace of this type.
    
            @param parent:
                The widget to use as a "parent" widget for any modal
                dialog(s) used during workspace address entry; None
                to use the GuiRoot.
            @return:
                The workspace address specified by the user; None 
                if the user has cancelled the process of workspace
                address entry.
        """
        try:
            dba = self.__db_type.enter_new_database_address(parent)
            raise NotImplementedError()
        except Exception as ex:
            raise WorkspaceError.wrap(ex)
