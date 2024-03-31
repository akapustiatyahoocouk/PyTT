from typing import Optional

from awt.MenuItem import MenuItem
from awt.Menu import Menu

class Submenu(MenuItem, Menu):

    ##########
    #   Construction
    def __init__(self, 
                 label: str,
                 hotkey: Optional[str] = None):
        MenuItem.__init__(self)
        Menu.__init__(self)

        assert isinstance(label, str)
        assert (hotkey is None) or isinstance(hotkey, str)

        self.__label = label
        self.__hotkey = hotkey
    
    ##########
    #   MenuItem (Properties)
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, lab: str) -> None:
        assert isinstance(label, str)
        self.__label = label

    @property
    def hotkey(self) -> str:
        return self.__hotkey

    @hotkey.setter
    def hotkey(self, new_hotkey: str) -> None:
        raise NotImplementedError()
    