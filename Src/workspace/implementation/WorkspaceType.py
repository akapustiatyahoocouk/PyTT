"""
    Defines the "Workspace type" ADT.
"""
#   Python standard library
from typing import final, Set

#   Dependencies on other PyTT components
from db.interface.api import *
from .Credentials import Credentials

#   Internal dependencies on modules within the same component
from .Exceptions import WorkspaceError

##########
#   Public entities
@final
class WorkspaceType:

    ##########
    #   Implementation
    __all = None
    __construction_permitted = False
    
    ##########
    #   Construction (internal only)
    def __init__(self, db_type: DatabaseType):
        assert WorkspaceType.__construction_permitted
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
            WorkspaceType.__construction_permitted = True
            WorkspaceType.__all = list()
            for db_type in DatabaseType.all:
                WorkspaceType.__all.append(WorkspaceType(db_type))
            WorkspaceType.__construction_permitted = False
        return set(WorkspaceType.__all)

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
            raise WorkspaceError.wrap(ex) from ex

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
        from .WorkspaceAddress import WorkspaceAddress
        try:
            db_address = self.__db_type.enter_new_database_address(parent)
            return WorkspaceAddress(db_address) if db_address else None
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Workspace handling
    def create_workspace(self, 
                         address: "WorkspaceAddress",
                         credentials: Optional[Credentials],
                         admin_user: Optional[str] = None,
                         admin_login: Optional[str] = None,
                         admin_password: Optional[str] = None) -> "Workspace":
        """
            Creates a new workspace at the specified address.
            The workspace is initially empty, except for a single 
            User with a single Account which has administrative 
            privileges.

            @param address:
                The address for the new workspace.
            @param credentials:
                The credentials to infer the properties of the 
                administrator user for the new workspace (optional).
            @param admin_user:
                The name for the workspace administrator User.
                If not None and credentials is not None, this parameter
                overrides the credentials.
            @param admin_login:
                The login for the workspace administrator Account.
                If not None and credentials is not None, this parameter
                overrides the credentials.
            @param admin_password:
                The password for the workspace administrator Account.
                If not None and credentials is not None, this parameter
                overrides the credentials.
            @return:
                The newly created and open workspace.
            @raise WorkspaceError:
                If the workspace creation fails for any reason.
        """
        from .Workspace import Workspace

        if credentials is not None:
            assert isinstance(credentials, Credentials)
            #   All other parameters are optional
            assert (admin_user is None) or isinstance(admin_user, str)
            assert (admin_login is None) or isinstance(admin_login, str)
            assert (admin_password is None) or isinstance(admin_password, str)
            admin_user = admin_user if admin_user else credentials._Credentials__login
            admin_login = admin_login if admin_login else credentials._Credentials__login
            admin_password = admin_password if admin_password else credentials._Credentials__password
        else:
            #   All other parameters are mandatory
            assert isinstance(admin_user, str)
            assert isinstance(admin_login, str)
            assert isinstance(admin_password, str)
        admin_user = admin_user.strip()
        admin_login = admin_login.strip()
        #   First the database...
        try:
            db = self.__db_type.create_database(address._WorkspaceAddress__db_address)
        except Exception as ex:
            raise WorkspaceError.wrap(ex) from ex
        #   ...then the admin user...
        #   ...then the admin account...
        #   ...and we're done
        return Workspace(address, db)

    ##########
    #   Operations (misc)
    @staticmethod
    def find_by_mnemonic(mnemonic: str) -> Optional["WorkspaceType"]:
        assert isinstance(mnemonic, str)
        
        for workspace_type in WorkspaceType.all:
            if workspace_type.mnemonic == mnemonic:
                return workspace_type
        return None
            
    @staticmethod
    def resolve(db_type: DatabaseType) -> "WorkspaceType":
        """
            Returns the WorkspaceType that corresponds to the
            specified DatabaseType.
            
            @param db_type:
                The database type to resolve to the workspace type.
            @return:
                The workspace type that represents the specified 
                database type.
        """
        assert isinstance(db_type, DatabaseType)

        for wt in WorkspaceType.all:
            if wt.__db_type is db_type:
                return wt
        #   The code below is a safety measure that should not
        #   normally be executed... ever! TODO log the warning    
        WorkspaceType.__construction_permitted = True
        wt = WorkspaceType(db_type)
        WorkspaceType.__construction_permitted = False
        WorkspaceType.__all.append(wt)
        return wt
