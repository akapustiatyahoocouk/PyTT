""" Database notifications. """

#   Python standard library
from typing import Any, TypeAlias, Callable
from threading import Thread

##########
#   Public entities
class Notification:
    """ The common base class for all Database notifications. """

    ##########
    #   Construction
    def __init__(self, database: "Database"):
        from .Database import Database
        assert isinstance(database, Database)
        self.__database = database

    ##########
    #   Properties
    @property
    def database(self) -> "Database":
        """ The Database where the change has occurred. """
        return self.__database

class DatabaseObjectCreatedNotification(Notification):
    """ Notifies interested parties that a new object has
        just been created in the database. """

    ##########
    #   Construction
    def __init__(self, database: "Database", obj: "DatabaseObject"):
        Notification.__init__(self, database)
        
        from .DatabaseObject import DatabaseObject
        assert isinstance(obj, DatabaseObject)

        self.__object = obj

    ##########
    #   Properties
    @property
    def object(self) -> "DatabaseObject":
        """ The newly created object. """
        return self.__object

class DatabaseObjectDestroyedNotification(Notification):
    """ Notifies interested parties that an object has
        just been destroyed in the database. """

    ##########
    #   Construction
    def __init__(self, database: "Database", obj: "DatabaseObject"):
        Notification.__init__(self, database)
        
        from .DatabaseObject import DatabaseObject
        assert isinstance(obj, DatabaseObject)

        self.__object = obj

    ##########
    #   Properties
    @property
    def object(self) -> "DatabaseObject":
        """ The destroyed object (aklready "dead" by the time
            this notification reaches interested parties!. """
        return self.__object

class DatabaseObjectModifiedNotification(Notification):
    """ Notifies interested parties that an object has
        just been modified in the database. """

    ##########
    #   Construction
    def __init__(self, database: "Database", obj: "DatabaseObject", property_name: str):
        Notification.__init__(self, database)
        
        from .DatabaseObject import DatabaseObject
        assert isinstance(obj, DatabaseObject)
        assert isinstance(property_name, str)

        self.__object = obj
        self.__property_name = property_name

    ##########
    #   Properties
    @property
    def object(self) -> "DatabaseObject":
        """ The modified object. """
        return self.__object

    @property
    def property_name(self) -> str:
        """ The name of the object's property that has been modified. """
        return self.__property_name

NotificationListener: TypeAlias = Callable[[Notification], None]
""" A signature of a listener to database notifications - a function
    or a bound method.
    IMPORTANT: will normally be called on a hidden "notification"
    thread running behind theDatabase. """

class NotificationHandler:

    ##########
    #   Operations
    def on_database_object_created(self, n: DatabaseObjectCreatedNotification) -> None:
        pass

    def on_database_object_destroyed(self, n: DatabaseObjectDestroyedNotification) -> None:
        pass

    def on_database_object_modified(self, n: DatabaseObjectModifiedNotification) -> None:
        pass
    