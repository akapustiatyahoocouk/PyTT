""" A menu item that presents a text and is optionally 
        bound with an Action. """
#   Python standard library
from typing import Optional
import tkinter as tk

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .KeyStroke import KeyStroke
from .MenuItem import MenuItem
from .Action import Action
from .ActionEvent import ActionEvent

##########
#   Public entities
class SimpleMenuItem(MenuItem):
    """ A menu item that presents a text and is optionally 
        bound with an Action. """

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
                except Exception:
                    tk_underline = None
                tk_menu.entryconfig(tk_menu_item_index, underline=tk_underline)
        #   Record the new hotkey
        self.__hotkey = new_hotkey

    @property
    def shortcut(self) -> str:
        """ The shortcut character of this menu item (underlined 
            in the UI); None if this menu item has no shortcut. """
        return self.__shortcut

    @shortcut.setter
    def shortcut(self, new_shortcut: KeyStroke) -> None:
        """ Sets the shortcut character of this menu item (underlined 
            in the UI); None for this menu item to have no shortcut. """
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

    ##########
    #   Tk event handlers
    def _on_tk_click(self): # TODO make private (with "__" prefix instead of "_"
        evt = ActionEvent(self)
        self.process_action_event(evt)
        return "break"
