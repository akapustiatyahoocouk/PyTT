#   Python standard library
from typing import Optional
import tkinter as tk

#   Internal dependencies on modules within the same component
from awt.KeyStroke import KeyStroke
from awt.MenuItem import MenuItem
from awt.Action import Action
from awt.ActionEvent import ActionEvent
from awt.PropertyChangeEvent import PropertyChangeEvent

class SimpleMenuItem(MenuItem):

    ##########    
    #   Construction
    def __init__(self, 
                 label: str,
                 hotkey: Optional[str] = None,
                 description: Optional[str] = None, 
                 shortcut: Optional[KeyStroke] = None,
                 image: Optional[tk.PhotoImage] = None,
                 action: Optional[Action] = None):
        MenuItem.__init__(self)
        
        assert isinstance(label, str)
        assert (hotkey is None) or isinstance(hotkey, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, KeyStroke)
        assert (image is None) or isinstance(image, tk.PhotoImage)
        assert (action is None) or isinstance(action, Action)

        self.__label = label
        self.__hotkey = hotkey
        self.__description = description
        self.__shortcut = shortcut
        self.__image = image
        self.__action = action
        
        #   Bind with Action
        if action is not None:
            action.add_property_change_listener(self.__on_action_property_changed)
            self.add_action_listener(action.execute)

    ##########
    #   MenuItem (Properties)
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

    @property
    def shortcut(self) -> str:
        return self.__shortcut

    @label.setter
    def shortcut(self, new_shortcut: KeyStroke) -> None:
        assert ((new_shortcut is None) or
                isinstance(new_shortcut, KeyStroke))
        
        if (self.menu is not None) and (new_shortcut != self.__shortcut):
            #   this menu item is part of the menu
            tk_menu : tk.Menu = self.menu._Menu__tk_impl
            tk_menu_item_index = self.menu.items._MenuItems__menu_items.index(self)
            if new_shortcut is None:
                tk_menu.entryconfig(tk_menu_item_index, accelerator=None)
            else:
                tk_menu.entryconfig(tk_menu_item_index, accelerator=str(new_shortcut))
        #   Record the new shortcut
        self.__shortcut = new_shortcut

    ##########
    #   Event listeners
    def __on_action_property_changed(self, evt: PropertyChangeEvent) -> None:
        match evt.changed_property:
            case Action.NAME_PROPERTY_NAME:
                self.label = self.__action.name
            case Action.HOTKEY_PROPERTY_NAME:
                self.hotkey = self.__action.hotkey
            case Action.SHORTCUT_PROPERTY_NAME:
                self.shortcut = self.__action.shortcut
            case Action.ENABLED_PROPERTY_NAME:
                self.enabled = self.__action.enabled
            case _:
                assert False    #   TODO implement other Action properties
    
    def _on_tk_click(self):
        evt = ActionEvent(self)
        self._process_action_event(evt)
