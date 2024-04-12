#   Python standard library
from typing import final

##########
#   Public entities
@final
class SqliteDatabaseLock:

    ##########
    #   Construction
    def __init__(self, path: str):
        """
            Creates a database lock directory.
            
            @param path:
                The full path to the lock directory.
            @raise DatabaseError:
                If the database lock could not be created).
        """
        assert isinstance(path, str)

