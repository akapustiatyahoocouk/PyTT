from typing import Optional

import awt_impl.KeyStroke
import awt_impl.MenuItem
import awt_impl.ActionEventProcessorMixin

class SimpleMenuItem(awt_impl.MenuItem.MenuItem):
    
    def __init__(self, 
                 label: str,
                 description: Optional[str] = None, 
                 shortcut: Optional[awt_impl.KeyStroke.KeyStroke] = None):
        awt_impl.MenuItem.MenuItem.__init__(self)
        
        assert isinstance(label, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, awt_impl.KeyStroke.KeyStroke)

        self.__label = label
        self.__description = description
        self.__shortcut = shortcut

    ##########
    #   MenuItem (Properties)
    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, lab: str) -> None:
        assert isinstance(label, str)
        self.__label = label

    ##########
    #   Implementation    
    def _on_tk_click(self):
        evt = awt_impl.ActionEvent.ActionEvent(self)
        self._process_action_event(evt)
