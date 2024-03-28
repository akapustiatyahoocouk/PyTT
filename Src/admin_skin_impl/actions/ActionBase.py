from typing import Optional

import awt
import admin_skin_impl.MainFrame

class ActionBase(awt.Action):
    """ The common base class for all "admin" skin actions. """
    
    ##########
    #   Construction
    def __init__(self, 
                 main_frame: admin_skin_impl.MainFrame.MainFrame,
                 name: str, 
                 description: Optional[str] = None, 
                 shortcut: Optional[awt.KeyStroke] = None):
        awt.Action.__init__(self, name=name, description=description, shortcut=shortcut)
        assert isinstance(main_frame, admin_skin_impl.MainFrame.MainFrame)
        
        self.__main_frame = main_frame
        
    ##########
    #   Properties
    @property
    def main_frame(self) -> "MainFrame":
        """ The MainFrame to which this Action is bound; never None. """
        return self.__main_frame
