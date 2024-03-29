from typing import final

from admin_skin_impl.MainFrame import MainFrame
from admin_skin_impl.actions.ExitAction import ExitAction
from admin_skin_impl.actions.AboutAction import AboutAction

@final
class ActionSet:
    
    def __init__(self, main_frame: MainFrame):
        self.__exit = ExitAction(main_frame)
        self.__about = AboutAction(main_frame)

    ##########
    #   Actions
    @property
    def exit(self) -> ExitAction:
        return self.__exit

    @property
    def about(self) -> AboutAction:
        return self.__about
    