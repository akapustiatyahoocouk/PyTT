import tkinter as tk

from typing import final, Any, Tuple
from abc import ABC

import awt_impl.MenuItem

@final
class MenuItems:
    ##########
    #   Construction
    def __init__(self, menu: "Menu"):
        self.__menu = menu
        self.__menu_items = list()
       
    ##########
    #   Operations
    def append(self, item: Any) -> awt_impl.MenuItem:
        import awt_impl.Submenu
        import awt_impl.Action
        import awt_impl.SimpleMenuItem
        
        assert item is not None
        if isinstance(item, str):
            #   menu.append('menu item text', **kwargs)
            #       Appending a string item to a menu
            (text_, underline_) = self.__process_label(item)
            text_menu_item = awt_impl.SimpleMenuItem.SimpleMenuItem(item)
            self.__menu._Menu__impl.add_command(label=text_, underline=underline_, command=text_menu_item._on_tk_click)
            self.__menu_items.append(text_menu_item)
            text_menu_item.__menu = self.__menu
            return text_menu_item
        
        elif (isinstance(item, awt_impl.Action.Action)):
            #   menu.append(action: Action, **kwargs)
            #       Appending an Action-based item to a menu
            #   TODO implement properly
            pass
            
        elif (isinstance(item, awt_impl.Submenu.Submenu)):
            #   menu.append(submenu: Submenu, **kwargs)
            #       Appending a sub-menu to a menu
            assert item._MenuItem__menu is None
            (text_, underline_) = self.__process_label(item.label)
            self.__menu._Menu__impl.add_cascade(label=text_, underline=underline_, menu=item._Menu__impl)
            self.__menu_items.append(item)
            item._Menu__impl.master = self.__menu._Menu__impl
            item._MenuItem__menu = self.__menu
            return item
        else:
            raise NotImplementedError()
     
    def remove_at(self, index: int) -> None:
        assert isinstance(index, int)
        self.__menu_items.remove(self.__menu_items[index])
        self.__menu._Menu__impl.delete(index)

    ##########
    #   Implementation helpers
    def __process_label(self, label: str) -> tuple[str, int]:
        text = ""
        underline = None
        i = 0
        while i < len(label):
            if (label[i] == "&") and (i + 1 < len(label)) and (label[i+1] == '&'):
                #   && -> &
                text += "&"
                i += 2;
            elif (label[i] == "&") and (i + 1 < len(label)) and (underline is None):
                underline = len(text)
                text += label[i+1]
                i += 2
            else:
                text += label[i]
                i += 1
        return (text, underline)

class Menu(ABC):
    """ A generic "Menu" is an ordered collection of MenuItems. """
    def __init__(self):
        self.__items = MenuItems(self)
        self.__impl = tk.Menu(tearoff=0)

    @property
    def items(self) -> MenuItems:
        return self.__items