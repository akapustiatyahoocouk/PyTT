""" Workspace notifications. """

#   Python standard library
from typing import Any, TypeAlias, Callable
from threading import Thread

##########
#   Public entities
class WorkspaceNotification:
    """ The common base class for all Workspace notifications. """

    ##########
    #   Construction
    def __init__(self, workspace: "Workspace"):
        from .Workspace import Workspace
        assert isinstance(workspace, Workspace)
        self.__workspace = workspace

    ##########
    #   Properties
    @property
    def workspace(self) -> "Workspace":
        """ The Workspace where the change has occurred. """
        return self.__workspace

class BusinessObjectCreatedNotification(WorkspaceNotification):
    """ Notifies interested parties that a new object has
        just been created in the workspace. """

    ##########
    #   Construction
    def __init__(self, workspace: "Workspace", obj: "BusinessObject"):
        WorkspaceNotification.__init__(self, workspace)
        
        from .BusinessObject import BusinessObject
        assert isinstance(obj, BusinessObject)

        self.__object = obj

    ##########
    #   Properties
    @property
    def object(self) -> "BusinessObject":
        """ The newly created object. """
        return self.__object

class BusinessObjectDestroyedNotification(WorkspaceNotification):
    """ Notifies interested parties that an object has
        just been destroyed in the workspace. """

    ##########
    #   Construction
    def __init__(self, workspace: "Workspace", obj: "BusinessObject"):
        WorkspaceNotification.__init__(self, workspace)
        
        from .BusinessObject import BusinessObject
        assert isinstance(obj, BusinessObject)

        self.__object = obj

    ##########
    #   Properties
    @property
    def object(self) -> "BusinessObject":
        """ The destroyed object (already "dead" by the time
            this notification reaches interested parties!. """
        return self.__object

class BusinessObjectModifiedNotification(WorkspaceNotification):
    """ Notifies interested parties that an object has
        just been modified in the workspace. """

    ##########
    #   Construction
    def __init__(self, workspace: "Workspace", obj: "BusinessObject", property_name: str):
        WorkspaceNotification.__init__(self, workspace)
        
        from .BusinessObject import BusinessObject
        assert isinstance(obj, BusinessObject)
        assert isinstance(property_name, str)

        self.__object = obj
        self.__property_name = property_name

    ##########
    #   Properties
    @property
    def object(self) -> "BusinessObject":
        """ The modified object. """
        return self.__object

    @property
    def property_name(self) -> str:
        """ The name of the object's property that has been modified. """
        return self.__property_name

WorkspaceNotificationListener: TypeAlias = Callable[[WorkspaceNotification], None]
""" A signature of a listener to workspace notifications - a function
    or a bound method.
    IMPORTANT: will normally be called on a hidden "notification"
    thread running behind the Workspace. """

class WorkspaceNotificationHandler:

    ##########
    #   Operations
    def on_workspace_object_created(self, n: BusinessObjectCreatedNotification) -> None:
        pass

    def on_workspace_object_destroyed(self, n: BusinessObjectDestroyedNotification) -> None:
        pass

    def on_workspace_object_modified(self, n: BusinessObjectModifiedNotification) -> None:
        pass
    