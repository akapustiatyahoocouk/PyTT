import tkinter as tk

from typing import final, Any, Tuple
from abc import ABC

from awt_impl.MenuItem import MenuItem

@final
class MenuItems:
    """ An ordered list of items in a Menu. """
    
    ##########
    #   Construction (private!)
    def __init__(self, menu: "Menu"):
        self.__menu = menu
        self.__menu_items = list()
       
    ##########
    #   Properties
    @property
    def menu(self) -> "Menu":
        """ The menu to which this list-of-menu-items belongs; never None. """
        return self.__menu

    ##########`
    #   Operations
    def append(self, item: Any, **kwargs) -> MenuItem:
        from awt_impl.Submenu import Submenu
        from awt_impl.Action import Action
        from awt_impl.SimpleMenuItem import SimpleMenuItem
        from awt_impl.KeyStroke import KeyStroke
        from awt_impl._TkHelpers import _tk_analyze_label
        
        assert item is not None
        if isinstance(item, str):
            #   menu.append('menu item text', **kwargs)
            #       Appending a string item to a menu
            #   TODO report unsupported kwargs
            (tk_text, tk_underline) = _tk_analyze_label(item)
            text_menu_item = SimpleMenuItem(item)
            self.__menu._Menu__tk_impl.add_command(label=tk_text, 
                                                   underline=tk_underline, 
                                                   command=text_menu_item._on_tk_click)
            self.__menu_items.append(text_menu_item)
            text_menu_item._MenuItem__menu = self.__menu
            return text_menu_item
        
        elif (isinstance(item, Action)):
            #   menu.append(action: Action, **kwargs)
            #       Appending an Action-based item to a menu
            #   TODO report unsupported kwargs
            action: Action = item
            #   Prepare properties for the menu item
            menu_item_label = kwargs.get("label", None)
            if not isinstance(menu_item_label, str):
                menu_item_label = action.name;
            menu_item_description = kwargs.get("description", None)
            if not isinstance(menu_item_description, str):
                menu_item_description = action.description;
            menu_item_shortcut = kwargs.get("shortcut", None)
            if not isinstance(menu_item_shortcut, KeyStroke):
                menu_item_shortcut = action.shortcut;
            #   Create menu item
            (tk_text, tk_underline) = _tk_analyze_label(menu_item_label)
            tk_accelerator = None
            if action.shortcut is not None:
                tk_accelerator = str(action.shortcut)
            simple_menu_item = SimpleMenuItem(menu_item_label,
                                              description=menu_item_description,
                                              shortcut=menu_item_shortcut,
                                              action=action)
            self.__menu._Menu__tk_impl.add_command(label=tk_text, 
                                                   underline=tk_underline, 
                                                   accelerator=tk_accelerator,
                                                   command=simple_menu_item._on_tk_click)
            self.__menu_items.append(simple_menu_item)
            simple_menu_item._MenuItem__menu = self.__menu
            #   Done creating the item
            return simple_menu_item
            
        elif (isinstance(item, Submenu)):
            #   menu.append(submenu: Submenu, **kwargs)
            #       Appending a sub-menu to a menu
            #   TODO report unsupported kwargs
            assert item.menu is None
            submenu: awt_impl.Submenu.Submenu = item
            #   Create menu item
            (tk_text, tk_underline) = _tk_analyze_label(submenu.label)
            self.__menu._Menu__tk_impl.add_cascade(label=tk_text, 
                                                   underline=tk_underline, 
                                                   menu=item._Menu__tk_impl)
            self.__menu_items.append(item)
            item._Menu__tk_impl.master = self.__menu._Menu__tk_impl
            item._MenuItem__menu = self.__menu
            return item

        else:
            raise NotImplementedError()
     
    def remove_at(self, index: int) -> None:
        assert isinstance(index, int)
        self.__menu_items.remove(self.__menu_items[index])
        self.__menu._Menu__tk_impl.delete(index)


class Menu(ABC):
    """ A generic "Menu" is an ordered collection of MenuItems. """
    
    ##########
    #   Construction
    def __init__(self):
        self.__items = MenuItems(self)
        self.__tk_impl = tk.Menu(tearoff=0)

    ##########
    #   Properties    
    @property
    def items(self) -> MenuItems:
        """ An ordered list of items in this Menu.
            Use this collection to manipulate this Menu's 
            contents (e.g. add items, etc.)"""
        return self.__items