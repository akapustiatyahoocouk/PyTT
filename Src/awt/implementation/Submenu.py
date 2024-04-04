#   Python standard library
from typing import Optional

#   Internal dependencies on modules within the same component
from awt.implementation.MenuItem import MenuItem
from awt.implementation.Menu import Menu

##########
#   Public entities
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
    #   MenuItem (Properties) TODO raise to MenuItem class ?
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, new_label: str) -> None:
        assert isinstance(new_label, str)
        
        if (self.menu is not None) and (new_label != self.__label):
            #   this menu item is part of the menu
            tk_menu : tk.Menu = self.menu._Menu__tk_impl
            tk_menu_item_index = self.menu.items._MenuItems__menu_items.index(self)
            tk_menu.entryconfig(tk_menu_item_index, label=new_label)
        #   Record the new label
        self.__label = new_label

    @property
    def hotkey(self) -> str:
        return self.__hotkey

    @hotkey.setter
    def hotkey(self, new_hotkey: str) -> None:
        assert (new_hotkey is None) or isinstance(new_hotkey, str)
        
        if (self.menu is not None) and (new_hotkey != self.__hotkey):
            #   this menu item is part of the menu
            tk_menu : tk.Menu = self.menu._Menu__tk_impl
            tk_menu_item_index = self.menu.items._MenuItems__menu_items.index(self)
            if new_hotkey is None:
                tk_menu.entryconfig(tk_menu_item_index, underline=None)
            else:
                try:
                    tk_underline = self.__label.lower().index(new_hotkey.lower())
                except:
                    tk_underline = None
                tk_menu.entryconfig(tk_menu_item_index, underline=tk_underline)
        #   Record the new hotkey
        self.__hotkey = new_hotkey
    