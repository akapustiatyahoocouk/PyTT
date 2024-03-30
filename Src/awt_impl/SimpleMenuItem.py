from ast import Or
from typing import Optional

from awt_impl.KeyStroke import KeyStroke
from awt_impl.MenuItem import MenuItem
from awt_impl.Action import Action
from awt_impl.ActionEvent import ActionEvent
from awt_impl.PropertyChangeEvent import PropertyChangeEvent
from awt_impl._TkHelpers import _tk_analyze_label

class SimpleMenuItem(MenuItem):

    ##########    
    #   Construction
    def __init__(self, 
                 label: str,
                 description: Optional[str] = None, 
                 shortcut: Optional[KeyStroke] = None,
                 action: Optional[Action] = None):
        MenuItem.__init__(self)
        
        assert isinstance(label, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, KeyStroke)
        assert (action is None) or isinstance(action, Action)

        self.__label = label
        self.__description = description
        self.__shortcut = shortcut
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
            (tk_text, tk_underline) = _tk_analyze_label(new_label)
            tk_menu.entryconfig(tk_menu_item_index, 
                                label=tk_text, 
                                underline=tk_underline)
        #   Record the new label
        self.__label = new_label

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
            case Action.SHORTCUT_PROPERTY_NAME:
                self.shortcut = self.__action.shortcut
            case Action.ENABLED_PROPERTY_NAME:
                self.enabled = self.__action.enabled
            case _:
                assert False    #   TODO implement other Action properties
    
    def _on_tk_click(self):
        evt = ActionEvent(self)
        self._process_action_event(evt)
