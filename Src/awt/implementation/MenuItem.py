#   Python standard library
from typing import Optional
from abc import ABC, abstractproperty, abstractmethod

#   Internal dependencies on modules within the same component
from awt.implementation.ActionEventProcessorMixin import ActionEventProcessorMixin

##########
#   Public entities
class MenuItem(ABC, ActionEventProcessorMixin):
    """ A generic "menu item" represents a single item within a menu. """

    ##########
    #   Construction
    def __init__(self):
        ABC.__init__(self)
        ActionEventProcessorMixin.__init__(self)

        self.__menu = None  #   ..to which this MenuItem belongs
        self.__enabled = True

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
        """ Sets the textual label of this menu item; cannot become None. """
        raise NotImplementedError()

    @abstractproperty
    def hotkey(self) -> str:
        """ The hotkey of this menu item, None if none. """
        raise NotImplementedError()

    @label.setter
    @abstractmethod
    def hotkey(self, hk: str) -> None:
        """ Sets the hotkey of this menu item; None for none. """
        raise NotImplementedError()

    @property
    def enabled(self) -> bool:
        """ True if this menu item is enabled, Fase if disabled; never None. """
        return self.__enabled

    @enabled.setter
    def enabled(self, new_enabled: bool) -> None:
        """ True to enable this menu item, False to disable; cannot become None. """
        assert isinstance(new_enabled, bool)
        
        if (self.__menu is not None) and (new_enabled != self.__enabled):
            #   this menu item is part of the menu
            self.__enabled = new_enabled
            tk_menu : tk.Menu = self.__menu._Menu__tk_impl
            tk_menu_item_index = self.__menu.items._MenuItems__menu_items.index(self)
            if new_enabled:
                tk_menu.entryconfig(tk_menu_item_index, state="normal")
            else:
                tk_menu.entryconfig(tk_menu_item_index, state="disabled")
        