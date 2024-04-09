"""
    Defines the "Workspace type" ADT.
"""
#   Python standard library
from typing import final, Set

#   Dependencies on other PyTT components
from db.interface.api import *

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
