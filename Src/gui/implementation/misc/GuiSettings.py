""" Persistent settings of the GUI. """

#   Python standard library
from typing import final, Optional;

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class GuiSettingsMeta(type):

    ##########
    #   Construction
    def __init__(cls, *args, **kwargs):
        type.__init__(cls, *args, **kwargs);

        cls.__impl = Settings.get("GUI")

    ##########
    #   Properties
    @property
    def last_login(cls) -> Optional[str]:
        """ The last used login identifier, None if not known. """
        return cls.__impl.get("last_login", "")

    @last_login.setter
    def last_login(cls, new_last_login: Optional[str]) -> None:
        """ Sets the last used login identifier, None for not known. """
        assert (new_last_login is None) or isinstance(new_last_login, str)
        
        if new_last_login is None:
            cls.__impl.remove("last_login")
        else:
            cls.__impl.put("last_login", new_last_login)

    @property
    def current_preferences(cls) -> Optional[Preferences]:
        """ The "current" Preferences in the Preferences dialog,
            None if there wasn't any. """
        qualified_name = cls.__impl.get("current_preferences", "")
        return GuiSettingsMeta.__find_preferences(Preferences.ROOT, qualified_name)        

    @current_preferences.setter
    def current_preferences(cls, new_current_preferences: Optional[Preferences]) -> None:
        """ Sets the "current" Preferences in the Preferences dialog,
            None if there isn't any. """
        assert (new_current_preferences is None) or isinstance(new_current_preferences, Preferences)
        
        if new_current_preferences is None:
            cls.__impl.remove("current_preferences")
        else:
            cls.__impl.put("current_preferences", new_current_preferences.qualified_name)
            
    ##########
    #   Implementation helpers
    @staticmethod
    def __find_preferences(parent: Preferences, qualified_name: str) -> Optional[Preferences]:
        if parent.qualified_name == qualified_name:
            return parent
        for child in parent.children:
            r = GuiSettingsMeta.__find_preferences(child, qualified_name)
            if r is not None:
                return r
        return None

@final
class GuiSettings(metaclass=GuiSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
