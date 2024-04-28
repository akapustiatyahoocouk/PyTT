""" A set of SQL records (rows) retrieved by a SELECT. """

#   Python standard library
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
        self.__current_row = 0
        
    ##########
    #   object
    def __len__(self) -> int:
        return len(self.__rows)
    
    def __iter__(self) -> "SqlRecordSet":
        self.__current_row = 0
        return self

    def __next__(self) -> SqlRecord:
        if self.__current_row < len(self.__rows):
            row = self.__rows[self.__current_row]
            self.__current_row += 1
            return SqlRecord(self, row)
        else:
            raise StopIteration

    ##########
    #   Implementation helpers
    def _get_column_index(self, column: str) -> Optional[int]:
        if self.__map_column_names_to_indices is None:
            self.__map_column_names_to_indices = dict()
            for i in range(len(self.__columns)):
                self.__map_column_names_to_indices[self.__columns[i]] = i
        return self.__map_column_names_to_indices.get(column, None)
                