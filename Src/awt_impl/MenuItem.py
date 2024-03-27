from abc import ABC, abstractproperty, abstractmethod

class MenuItem(ABC):
    """ A generic "menu item" represents a single item within a menu. """

    ##########
    #   Construction
    def __init__(self):
        pass

    ##########
    #   Properties
    @abstractproperty
    def label(self) -> str:
        raise NotImplementedError()

    @label.setter
    @abstractmethod
    def label(self, lab: str) -> None:
        raise NotImplementedError()
        