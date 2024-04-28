#   Python standard library
from typing import final

#   Dependencies on other PyTT components
import db.interface.api as dbapi

#   Internal dependencies on modules within the same component
from .WorkspaceType import WorkspaceType

##########
#   Public entities
@final
class WorkspaceAddress:

    ##########
    #   Construction internal only)
    def __init__(self, db_address: dbapi.DatabaseAddress):
        assert isinstance(db_address, dbapi.DatabaseAddress)

        self.__db_address = db_address

    ##########
    #   object
    def __str__(self) -> str:
        return self.display_form

    def __eq__(self, op2: "WorkspaceAddress") -> bool:
        if not isinstance(op2, WorkspaceAddress):
            return False
        return self.__db_address == op2.__db_address

    def __ne__(self, op2: "WorkspaceAddress") -> bool:
        if not isinstance(op2, WorkspaceAddress):
            return True
        return self.__db_address != op2.__db_address

    ##########
    #   Properties
    @property
    def workspace_type(self) -> WorkspaceType:
        """ The workspace type to which this workspace address belongs. """
        return WorkspaceType.resolve(self.__db_address.database_type)

    @property
    def display_form(self) -> str:
        """ The user-readable display form of this workspace address. """
        return self.__db_address.display_form

    @property
    def external_form(self) -> str:
        """ The external (re-parsable) form of this workspace address. """
        return self.__db_address.external_form
