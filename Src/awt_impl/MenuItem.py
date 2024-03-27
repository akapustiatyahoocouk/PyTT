from abc import ABC, abstractproperty, abstractmethod

import awt_impl.ActionEventProcessorMixin

class MenuItem(ABC,
               awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin):
    """ A generic "menu item" represents a single item within a menu. """

    ##########
    #   Construction
    def __init__(self):
        ABC.__init__(self)
        awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin.__init__(self)
        self.__menu = None

    ##########
    #   Properties
    @property
    def menu(self) -> "Menu":
        """ The Menu to which this MenuItem belongs; None is this
            is a standalone menu item (i.e. not part of any menu. """
        return self.__menu

    @abstractproperty
    def label(self) -> str:
        """ The textual label of this menu item; never None. """
        raise NotImplementedError()

    @label.setter
    @abstractmethod
    def label(self, lab: str) -> None:
        """ Sets the textual label of this menu item; cannot be None. """
        raise NotImplementedError()
        