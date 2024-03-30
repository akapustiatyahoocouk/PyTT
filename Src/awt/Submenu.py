from awt.MenuItem import MenuItem
from awt.Menu import Menu

class Submenu(MenuItem, Menu):

    ##########
    #   Construction
    def __init__(self, label: str):
        MenuItem.__init__(self)
        Menu.__init__(self)

        assert isinstance(label, str)
        self.__label = label
    
    ##########
    #   MenuItem (Properties)
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, lab: str) -> None:
        assert isinstance(label, str)
        self.__label = label
    