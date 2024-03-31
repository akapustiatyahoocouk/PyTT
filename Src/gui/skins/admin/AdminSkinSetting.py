"""
    Persistent settings of the Admin skin.
"""
from typing import final

from util.Annotations import staticproperty
from util.ComponentSettings import ComponentSettings
from util.Settings import Settings

@final
class AdminSkinSettings:
    """ Persistent settings. """

    ##########
    #   Implementation
    __impl: ComponentSettings = Settings.get("AdminSkin")

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty
    def main_frame_x() -> int:
        pass
        