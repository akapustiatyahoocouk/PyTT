
from awt_impl.MenuItem import MenuItem

class SimpleMenuItem(MenuItem):
    
    def __init__(self, label: str):
        MenuItem.__init__(self)
        
        assert isinstance(label, str)
        self.__label = label

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
