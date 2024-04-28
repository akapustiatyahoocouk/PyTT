""" Defines exceptions thrown by the high-level (business storage) workspace API. """

##########
#   Public entities
class WorkspaceError(Exception):
    """ The common base class for all workspace.api - level exceptions. """

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
    @staticmethod
    def wrap(ex: Exception) -> "WorkspaceError":
        if isinstance(ex, WorkspaceError):
            return ex
        result = WorkspaceError(str(ex))
        result.__cause__ = ex
        return result

class InvalidWorkspaceAddressError(WorkspaceError):
    """ Thrown when an invalid workspace address is supplied to a db API service. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__('Invalid workspace address')

class AccessDeniedError(WorkspaceError):
    """ Thrown when a login attempt fails. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__("Access denied")
