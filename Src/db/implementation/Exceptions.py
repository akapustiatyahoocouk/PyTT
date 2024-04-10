"""
    Defines exceptions thrown by the low-level (data storage) database API.
"""

##########
#   Public entities
class DatabaseError(Exception):
    """ The common base class for all db.api - level exceptions. """
    
    ##########
    #   Construction
    def __init__(self, message: str):
        self.__message = message

    ##########
    #   object
    def __str__(self) -> str:
        return self.__message


class InvalidDatabaseAddressError(DatabaseError):
    """ Thrown when an invalid database address is supplied to a db API service. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__('Invalid database address')

class DatabaseIoError(DatabaseError):
    """ Thrown when an db API service fails due to an underlying
        I/O or database engine. """

    ##########
    #   Construction
    def __init__(self, message: str):
        super().__init__(message)
