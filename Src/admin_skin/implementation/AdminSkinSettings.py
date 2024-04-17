"""
    Persistent settings of the Admin skin.
"""
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
class AdminSkinSettingsMeta(type):
    """ The metaclass for AdminSkinSettings which implements
        gettable/settable static properties there. """

    ##########
    #   Construction
    def __init__(self, *args, **kwargs):
        type.__init__(self, *args, **kwargs)

        self.__impl = Settings.get("AdminSkin")

    ##########
    #   Properties
    @property
    def main_frame_x(self) -> int:
        """ The X-coordinate of the main frame's top-left corner. """
        return self.__impl.get_int("main_frame_x", 64)

    @main_frame_x.setter
    def main_frame_x(self, new_x: int) -> None:
        """ Sets the X-coordinate of the main frame's top-left corner. """
        assert isinstance(new_x, int)
        self.__impl.put_int("main_frame_x", new_x)

    @property
    def main_frame_y(self) -> int:
        """ The Y-coordinate of the main frame's top-left corner. """
        return self.__impl.get_int("main_frame_y", 64)

    @main_frame_y.setter
    def main_frame_y(self, new_y: int) -> None:
        """ Sets the Y-coordinate of the main frame's top-left corner. """
        assert isinstance(new_y, int)
        self.__impl.put_int("main_frame_y", new_y)

    @property
    def main_frame_width(self) -> int:
        """ The width of the main frame. """
        return self.__impl.get_int("main_frame_width", 480)

    @main_frame_width.setter
    def main_frame_width(self, new_width: int) -> None:
        """ Sets the width of the main frame. """
        assert isinstance(new_width, int)
        self.__impl.put_int("main_frame_width", new_width)

    @property
    def main_frame_height(self) -> int:
        """ The height of the main frame. """
        return self.__impl.get_int("main_frame_height", 320)

    @main_frame_height.setter
    def main_frame_height(self, new_height: int) -> None:
        """ Sets the height of the main frame. """
        assert isinstance(new_height, int)
        self.__impl.put_int("main_frame_height", new_height)

    @property
    def main_frame_maximized(self) -> bool:
        """ True if the main frame is maximized, else False. """
        return self.__impl.get_bool("main_frame_maximized", False)

    @main_frame_maximized.setter
    def main_frame_maximized(self, new_maximized: bool) -> None:
        """ Set to True if the main frame is maximized, else to False. """
        assert isinstance(new_maximized, bool)
        self.__impl.put_bool("main_frame_maximized", new_maximized)

@final
class AdminSkinSettings(metaclass=AdminSkinSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
