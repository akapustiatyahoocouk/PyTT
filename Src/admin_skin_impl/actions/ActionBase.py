from typing import Optional

from awt import Action, KeyStroke
from admin_skin_impl.MainFrame import MainFrame

class ActionBase(Action):
    """ The common base class for all "admin" skin actions. """
    
    ##########
    #   Construction
    def __init__(self, 
                 main_frame: MainFrame,
                 name: str, 
                 description: Optional[str] = None, 
                 shortcut: Optional[KeyStroke] = None):
        Action.__init__(self, name=name, description=description, shortcut=shortcut)
        assert isinstance(main_frame, MainFrame)
        
        self.__main_frame = main_frame
        
    ##########
    #   Properties
    @property
    def main_frame(self) -> "MainFrame":
        """ The MainFrame to which this Action is bound; never None. """
        return self.__main_frame
