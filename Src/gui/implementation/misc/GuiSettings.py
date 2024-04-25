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

@final
class GuiSettings(metaclass=GuiSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
