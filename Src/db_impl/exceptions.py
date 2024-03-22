"""
    Defines exceptions thrown by the low-level (data storage) database API.
"""

class DatabaseException(Exception):
    """ The common base class for all db.api - level exceptions. """
    
    ##########
    #   Construction
    def __init__(self, message: str):
        self.__message = message

    ##########
    #   object
    def __str__(self) -> str:
        return self.__message


class InvalidDatabaseAddressException(DatabaseException):
    """ Thrown when an invalid database address is supplied to a db API service. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__('Invalid database address')
    