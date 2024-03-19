"""
    Defines exceptions thrown by the low-level (data storage) database API.
"""

class DatabaseException(Exception):
    
    def __init__(self, message: str):
        self.__message = message

    def __str__(self):
        return self.__message

