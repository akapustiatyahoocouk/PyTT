""" A single SQL record (rows) retrieved by a SELECT. """

#   Python standard library
from typing import Any
from enum import Enum

#   Dependencies on other PyTT components
from db.interface.api import *

##########
#   Public entities
class SqlRecord:
    """ A single SQL record (rows) retrieved by a SELECT. """

    ##########
    #   Construction
    def __init__(self, rs: "SqlRecordSet", row: tuple) -> None:
        
        self.__rs = rs
        self.__row = row

    ##########
    #   object
    def __getitem__(self, key) -> Any:
        if isinstance(key, int):
            try:
                return self.__row[key]
            except Exception as ex:
                raise DoesNotExistErrorDoesNotExistError("field", "index", key)
        elif isinstance(key, str):
            index = self.__rs._get_column_index(key)
            if index is None:
                raise DoesNotExistErrorDoesNotExistError("field", "index", key)
            return self.__row[index]
        else:
            raise DoesNotExistErrorDoesNotExistError("field", "index", key)