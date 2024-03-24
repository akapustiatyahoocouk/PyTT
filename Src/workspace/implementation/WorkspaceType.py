""" Defines the "Workspace type" ADT. """
#   Python standard library
from typing import final, Set

#   Dependencies on other PyTT components
import db.interface.api as dbapi
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Credentials import Credentials
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
    def __init__(self, db_type: dbapi.DatabaseType):
        assert WorkspaceType.__construction_permitted
        assert isinstance(db_type, dbapi.DatabaseType)

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
            WorkspaceType.__all = []
            for db_type in dbapi.DatabaseType.all:
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
        from .WorkspaceAddress import WorkspaceAddress
        
        try:
            db_address = self.__db_type.parse_database_address(external_form)
            return WorkspaceAddress(db_address)
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

    def enter_existing_workspace_address(self, parent: tk.BaseWidget) -> "WorkspaceAddress":
        """
            Prompts the user to interactively specify an address
            of an existing workspace of this type.

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
            db_address = self.__db_type.enter_existing_database_address(parent)
            return WorkspaceAddress(db_address) if db_address else None
        except Exception as ex:
            raise WorkspaceError.wrap(ex)

    ##########
    #   Workspace handling
    def create_workspace(self,
                         address: "WorkspaceAddress",
                         admin_user: str,
                         admin_login: str,
                         admin_password: str) -> "Workspace":
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

        #   All parameters are mandatory
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
        try:
            user = db.create_user(real_name=admin_user)
        except Exception as ex:
            try:
                db.close()
            except:
                pass    #   TODO log
            raise WorkspaceError.wrap(ex) from ex
        #   ...then the admin account...
        try:
            account = user.create_account(login=admin_login,
                                          password=admin_password,
                                          capabilities=dbapi.Capabilities.ADMINISTRATOR)
        except Exception as ex:
            try:
                db.close()
            except:
                pass    #   TODO log
            raise WorkspaceError.wrap(ex) from ex
        #   ...and we're done
        return Workspace(address, db)

    def open_workspace(self,
                       address: "WorkspaceAddress") -> "Workspace":
        """
            Opens an existingworkspace at the specified address.
            The workspace is always opened successfully if the
            underlying database opens successfully, but it may
            or may not permit access with the e.g. current
            credentials.

            @param address:
                The address of an existing workspace.
                overrides the credentials.
            @return:
                The newly open workspace.
            @raise WorkspaceError:
                If the workspace opening fails for any reason.
        """
        from .Workspace import Workspace

        #   First the database...
        try:
            db = self.__db_type.open_database(address._WorkspaceAddress__db_address)
        except Exception as ex:
            raise WorkspaceError.wrap(ex) from ex
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
    def resolve(db_type: dbapi.DatabaseType) -> "WorkspaceType":
        """
            Returns the WorkspaceType that corresponds to the
            specified DatabaseType.

            @param db_type:
                The database type to resolve to the workspace type.
            @return:
                The workspace type that represents the specified
                database type.
        """
        assert isinstance(db_type, dbapi.DatabaseType)

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
