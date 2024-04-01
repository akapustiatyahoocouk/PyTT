"""
    Defines a "resource factory" an agent responsible
    for creation of localizable resources.
"""
from abc import ABC

from util.Locale import Locale

class ResourceFactory(ABC):
    """ An agent responsible for creation of localizable resources. """
    
    ##########
    #   Operations
    def get_string(self, key: str, locale: Locale = Locale.default) -> str:
        assert isinstance(key, str)
