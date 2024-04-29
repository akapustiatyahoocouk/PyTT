#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from .ViewType import ViewType
from .UsersViewType import UsersViewType
from .View import View

##########
#   Public entities
class UsersView(View):
    
    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget) -> None:
        View.__init__(self, parent)

    ##########
    #   Properties
    @property
    def type(self) -> ViewType:
        return UsersViewType.instance
    