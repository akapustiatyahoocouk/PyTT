""" A single SQL record (rows) retrieved by a SELECT. """

#   Python standard library
from typing import Any
from enum import Enum

#   Dependencies on other PyTT components
from db.interface.api import *

#   Internal dependencies on modules within the same component
from .SqlDataType import SqlDataType

##########
#   Public entities
class SqlRecord:
    """ A single SQL record (rows) retrieved by a SELECT. """

    ##########
    #   Construction
    def __init__(self, rs: "SqlRecordSet", row_number: int, row: tuple) -> None:
        from .SqlRecordSet import SqlRecordSet
        assert isinstance(rs, SqlRecordSet)
        assert isinstance(row_number, int)
        assert isinstance(row, tuple)
        
        self.__rs = rs
        self.__row_number = row_number
        self.__row = row

    ##########
    #   object
    def __getitem__(self, key_and_type) -> Any:
        """ Raises ValueError if an error occurs """
        if isinstance(key_and_type, tuple):
            assert (len(key_and_type) == 2 and 
                    isinstance(key_and_type[1], SqlDataType))
            key = key_and_type[0]
            data_type = key_and_type[1]
        else:
            key = key_and_type
            data_type = None
        #   Extract the value from the required column...
        raw_result = None
        if isinstance(key, int):
            try:
                raw_result = self.__row[key]
            except Exception as ex:
                raise DatabaseObjectDoesNotExistError("field", "index", key)
        elif isinstance(key, str):
            index = self.__rs._SqlRecordSet__get_column_index(key)
            if index is None:
                raise DatabaseObjectDoesNotExistError("field", "index", key)
            raw_result = self.__row[index]
        else:
            raise DatabaseObjectDoesNotExistError("field", "index", key)
        #   ...and convert is to the required value
        if (data_type is None) or (raw_result is None):
            return raw_result
        match data_type:
            case SqlDataType.INTEGER:
                return int(raw_result)
            case SqlDataType.REAL:
                return float(raw_result)
            case SqlDataType.STRING:
                return str(raw_result)
            case SqlDataType.BOOLEAN:
                if raw_result == "Y":
                    return True
                elif raw_result == "N":
                    return False
                else:
                    raise ValueError()
            case _:
                raise NotImplementedError()
                