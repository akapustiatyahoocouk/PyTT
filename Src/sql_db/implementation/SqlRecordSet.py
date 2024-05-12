""" A set of SQL records (rows) retrieved by a SELECT. """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import Optional
from enum import Enum

#   Internal dependencies on modules within the same component
from .SqlRecord import SqlRecord

##########
#   Public entities
class SqlRecordSet:
    """ A set of SQL records (rows) retrieved by a SELECT. """

    ##########
    #   Construction
    def __init__(self, columns, rows) -> None:
        
        self.__columns = columns
        self.__rows = rows
        self.__map_column_names_to_indices = None   # lazily prepared dict()
        
    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__rows)
    
    def __getitem__(self, index: int) -> SqlRecord:
        assert isinstance(index, int)
        return SqlRecord(self, index, self.__rows[index])

    def __iter__(self) -> SqlRecordSet:
        class Iterator:
            def __init__(self, rs):
                self.__rs = rs
                self.__current_row_index = 0
            def __next__(self) -> SqlRecord:
                if self.__current_row_index < len(self.__rs._SqlRecordSet__rows):
                    row_number = self.__current_row_index
                    row = self.__rs._SqlRecordSet__rows[row_number]
                    self.__current_row_index += 1
                    return SqlRecord(self.__rs, row_number, row)
                else:
                    raise StopIteration
        return Iterator(self)

    ##########
    #   Implementation helpers
    def __get_column_index(self, column: str) -> Optional[int]:
        if self.__map_column_names_to_indices is None:
            self.__map_column_names_to_indices = dict()
            for i in range(len(self.__columns)):
                self.__map_column_names_to_indices[self.__columns[i]] = i
        return self.__map_column_names_to_indices.get(column, None)
                