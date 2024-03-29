from ast import Or
from typing import Optional

import tkinter as tk

import awt_impl.KeyStroke
import awt_impl.MenuItem
import awt_impl.Action
import awt_impl.ActionEventProcessorMixin
import awt_impl.PropertyChangeEvent
import awt_impl._TkHelpers

class SimpleMenuItem(awt_impl.MenuItem.MenuItem):
    
    def __init__(self, 
                 label: str,
                 description: Optional[str] = None, 
                 shortcut: Optional[awt_impl.KeyStroke.KeyStroke] = None,
                 action: Optional[awt_impl.Action] = None):
        awt_impl.MenuItem.MenuItem.__init__(self)
        
        assert isinstance(label, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, awt_impl.KeyStroke.KeyStroke)
        assert (action is None) or isinstance(action, awt_impl.Action.Action)

        self.__label = label
        self.__description = description
        self.__shortcut = shortcut
        self.__action = action
        
        #   Bind with Action
        if self.__action is not None:
            self.__action.add_property_change_listener(self.__on_action_property_changed)

    ##########
    #   MenuItem (Properties)
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, new_label: str) -> None:
        assert isinstance(new_label, str)
        
        if (self._MenuItem__menu is not None) and (new_label != self.__label):
            #   this menu item is part of the menu
            tk_menu : tk.Menu = self._MenuItem__menu._Menu__impl
            tk_menu_item_index = self._MenuItem__menu._Menu__items._MenuItems__menu_items.index(self)
            (tk_text, tk_underline) = awt_impl._TkHelpers._analyze_label(new_label)
            tk_menu.entryconfig(tk_menu_item_index, 
                                label=tk_text, 
                                underline=tk_underline)
        #   Record the new label
        self.__label = new_label

    @property
    def shortcut(self) -> str:
        return self.__shortcut

    @label.setter
    def shortcut(self, new_shortcut: awt_impl.KeyStroke.KeyStroke) -> None:
        assert ((new_shortcut is None) or
                isinstance(new_shortcut, awt_impl.KeyStroke.KeyStroke))
        
        if (self._MenuItem__menu is not None) and (new_shortcut != self.__shortcut):
            #   this menu item is part of the menu
            tk_menu : tk.Menu = self._MenuItem__menu._Menu__impl
            tk_menu_item_index = self._MenuItem__menu._Menu__items._MenuItems__menu_items.index(self)
            if new_shortcut is None:
                tk_menu.entryconfig(tk_menu_item_index, accelerator=None)
            else:
                tk_menu.entryconfig(tk_menu_item_index, accelerator=str(new_shortcut))
        #   Record the new shortcut
        self.__shortcut = new_shortcut

    ##########
    #   Implementation    
    def __on_action_property_changed(self, evt: awt_impl.PropertyChangeEvent.PropertyChangeEvent) -> None:
        match evt.changed_property:
            case awt_impl.Action.Action.NAME_PROPERTY_NAME:
                self.label = self.__action.name
            case awt_impl.Action.Action.SHORTCUT_PROPERTY_NAME:
                self.shortcut = self.__action.shortcut
            case awt_impl.Action.Action.ENABLED_PROPERTY_NAME:
                self.enabled = self.__action.enabled
            case _:
                assert False    #   TODO implement other Action properties
    
    def _on_tk_click(self):
        evt = awt_impl.ActionEvent.ActionEvent(self)
        self._process_action_event(evt)
