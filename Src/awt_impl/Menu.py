from distutils.util import execute
import tkinter as tk

from typing import final, Any, Tuple
from abc import ABC

import awt_impl.MenuItem
import awt_impl._TkHelpers

@final
class MenuItems:
    """ An ordered list of items in a Menu. """
    
    ##########
    #   Construction (private!)
    def __init__(self, menu: "Menu"):
        self.__menu = menu
        self.__menu_items = list()
       
    ##########`
    #   Operations
    def append(self, item: Any, **kwargs) -> awt_impl.MenuItem.MenuItem:
        import awt_impl.Submenu
        import awt_impl.Action
        import awt_impl.SimpleMenuItem
        import awt_impl.KeyStroke
        
        assert item is not None
        if isinstance(item, str):
            #   menu.append('menu item text', **kwargs)
            #       Appending a string item to a menu
            #   TODO report unsupported kwargs
            (text_, underline_) = awt_impl._TkHelpers._analyze_label(item)
            text_menu_item = awt_impl.SimpleMenuItem.SimpleMenuItem(item)
            self.__menu._Menu__impl.add_command(label=text_, underline=underline_, command=text_menu_item._on_tk_click)
            self.__menu_items.append(text_menu_item)
            text_menu_item._MenuItem__menu = self.__menu
            return text_menu_item
        
        elif (isinstance(item, awt_impl.Action.Action)):
            #   menu.append(action: Action, **kwargs)
            #       Appending an Action-based item to a menu
            #   TODO report unsupported kwargs
            action: awt_impl.Action.Action = item
            #   Prepare properties for the menu item
            menu_item_label = kwargs.get("label", None)
            if not isinstance(menu_item_label, str):
                menu_item_label = action.name;
            menu_item_description = kwargs.get("description", None)
            if not isinstance(menu_item_description, str):
                menu_item_description = action.description;
            menu_item_shortcut = kwargs.get("shortcut", None)
            if not isinstance(menu_item_shortcut, awt_impl.KeyStroke.KeyStroke):
                menu_item_shortcut = action.shortcut;
            #   Create menu item
            (tk_text, tk_underline) = awt_impl._TkHelpers._analyze_label(menu_item_label)
            tk_accelerator = None
            if action.shortcut is not None:
                tk_accelerator = str(action.shortcut)
            simple_menu_item = awt_impl.SimpleMenuItem.SimpleMenuItem(menu_item_label,
                                                                      description=menu_item_description,
                                                                      shortcut=menu_item_shortcut,
                                                                      action=action)
            self.__menu._Menu__impl.add_command(label=tk_text, 
                                                underline=tk_underline, 
                                                accelerator=tk_accelerator,
                                                command=simple_menu_item._on_tk_click)
            self.__menu_items.append(simple_menu_item)
            simple_menu_item._MenuItem__menu = self.__menu
            #   Bind menu item with the action
            simple_menu_item.add_action_listener(action.execute)
            #   TODO make simple_menu_item listen to action property changes
            action.add_property_change_listener
            #   Done creating the item
            return simple_menu_item
            
        elif (isinstance(item, awt_impl.Submenu.Submenu)):
            #   menu.append(submenu: Submenu, **kwargs)
            #       Appending a sub-menu to a menu
            #   TODO report unsupported kwargs
            assert item._MenuItem__menu is None
            submenu: awt_impl.Submenu.Submenu = item
            #   Create menu item
            (text_, underline_) = awt_impl._TkHelpers._analyze_label(submenu.label)
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


class Menu(ABC):
    """ A generic "Menu" is an ordered collection of MenuItems. """
    
    ##########
    #   Construction
    def __init__(self):
        self.__items = MenuItems(self)
        self.__impl = tk.Menu(tearoff=0)

    ##########
    #   Properties    
    @property
    def items(self) -> MenuItems:
        """ An ordered list of items in this Menu.
            Use this collection to manipulate this Menu's 
            contents (e.g. add items, etc.)"""
        return self.__items