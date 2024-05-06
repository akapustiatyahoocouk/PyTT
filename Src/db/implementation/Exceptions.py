""" Defines exceptions thrown by the low-level (data storage) database API. """
from typing import Any

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
    
    ##########
    #   Operations
    def wrap(ex: Exception) -> "DatabaseError":
        assert isinstance(ex, Exception)

        if isinstance(ex, DatabaseError):
            return ex
        dberr = DatabaseError(str(ex))
        dberr.__cause__ = ex
        return dberr

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

class DatabaseObjectAlreadyExistsError(DatabaseError):
    """ Thrown when an db API service fails because it tries to
        create an object whose "must be unique" property
        matches that of an already existing object. """

    ##########
    #   Construction
    def __init__(self, object_type_name: str, property_name:str, property_value: Any):
        super().__init__("The " + object_type_name +
                         " with '" + property_name + "' = '" + str(property_value) +
                         "' already exists")

class DatabaseObjectDoesNotExistError(DatabaseError):
    """ Thrown when an db API service fails because it tries to
        access an object whose "must be unique" property
        does not match that of any already existing object. """

    ##########
    #   Construction
    def __init__(self, object_type_name: str, property_name:str, property_value: Any):
        super().__init__("The " + object_type_name +
                         " with '" + property_name + "' = '" + str(property_value) +
                         "' does not exist")

class InvalidDatabaseObjectPropertyError(DatabaseError):
    """ Thrown when an db API service fails because it tries to
        set a property of a database object toan invalie value. """

    ##########
    #   Construction
    def __init__(self, object_type_name: str, property_name:str, property_value: Any):
        super().__init__("Property '" + property_name + "' of " + object_type_name +
                         " cannot be set to '" + str(property_value) + "'")

class DatabaseAccessDeniedError(DatabaseError):
    """ Thrown when a login attempt fails. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__("Access denied")

class DatabaseObjectDeadError(DatabaseError):
    """ Thrown when an attempt is made to use a "dead" object. """

    ##########
    #   Construction
    def __init__(self, object_type_name: str):
        super().__init__("The " + object_type_name + " is dead")
