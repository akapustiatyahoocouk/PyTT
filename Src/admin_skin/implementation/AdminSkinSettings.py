"""
    Persistent settings of the Admin skin.
"""
from typing import final

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
class AdminSkinSettingsMeta(type):

    ##########
    #   Construction
    def __init__(self, *args, **kwargs):
        type.__init__(self, *args, **kwargs);
        
        self.__impl = Settings.get("AdminSkin")

    ##########
    #   Properties
    @property
    def main_frame_x(self) -> int:
        return self.__impl.get_int("main_frame_x", 64)

    @main_frame_x.setter
    def main_frame_x(self, new_x: int) -> None:
        assert isinstance(new_x, int)
        self.__impl.put_int("main_frame_x", new_x)

    @property
    def main_frame_y(self) -> int:
        return self.__impl.get_int("main_frame_y", 64)

    @main_frame_y.setter
    def main_frame_y(self, new_y: int) -> None:
        assert isinstance(new_y, int)
        self.__impl.put_int("main_frame_y", new_y)

    @property
    def main_frame_width(self) -> int:
        return self.__impl.get_int("main_frame_width", 480)

    @main_frame_width.setter
    def main_frame_width(self, new_width: int) -> None:
        assert isinstance(new_width, int)
        self.__impl.put_int("main_frame_width", new_width)

    @property
    def main_frame_height(self) -> int:
        return self.__impl.get_int("main_frame_height", 320)

    @main_frame_height.setter
    def main_frame_height(self, new_height: int) -> None:
        assert isinstance(new_height, int)
        self.__impl.put_int("main_frame_height", new_height)

    @property
    def main_frame_maximized(self) -> bool:
        return self.__impl.get_bool("main_frame_maximized", False)

    @main_frame_maximized.setter
    def main_frame_maximized(self, new_maximized: bool) -> None:
        assert isinstance(new_maximized, bool)
        self.__impl.put_bool("main_frame_maximized", new_maximized)

@final
class AdminSkinSettings(metaclass=AdminSkinSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
