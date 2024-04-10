"""
    Defines exceptions thrown by the high-level (business storage) workspace API.
"""

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
        #   TODO implement properly
        raise WorkspaceError(str(ex))   


class InvalidWorkspaceAddressError(WorkspaceError):
    """ Thrown when an invalid workspace address is supplied to a db API service. """

    ##########
    #   Construction
    def __init__(self):
        super().__init__('Invalid workspace address')
