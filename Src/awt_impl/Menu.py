import tkinter as tk

from typing import final, Any, Tuple
from abc import ABC

import awt_impl.MenuItem
import awt_impl.TextMenuItem

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
        assert item is not None
        if isinstance(item, str):
            #   Appending a string item to a menu
            (text_, underline_) = self.__process_label(item)
            text_menu_item = awt_impl.TextMenuItem.TextMenuItem(item)
            self.__menu._impl.add_command(label=text_, underline=underline_, command=text_menu_item._on_tk_click)
            self.__menu_items.append(text_menu_item)
            return text_menu_item
        elif (item.__class__.__name__ == "Submenu" and
              item.__module__ == "awt_impl.Submenu"):
            #   Appending a sub-menu to a menu
            (text_, underline_) = self.__process_label(item.label)
            self.__menu._impl.add_cascade(label=text_, underline=underline_, menu=item._impl)
            self.__menu_items.append(item)
            item._impl.master = self.__menu._impl
            return item
        else:
            raise NotImplementedError()
     
    def remove_at(self, index: int) -> None:
        assert isinstance(index, int)
        self.__menu_items.remove(self.__menu_items[index])
        self.__menu._impl.delete(index)

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
        self._impl = tk.Menu(tearoff=0)

    @property
    def items(self) -> MenuItems:
        return self.__items