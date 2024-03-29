from typing import final

import admin_skin_impl.MainFrame
import admin_skin_impl.actions.ExitAction
import admin_skin_impl.actions.AboutAction

@final
class ActionSet:
    
    def __init__(self,
                 main_frame: admin_skin_impl.MainFrame.MainFrame):
        self.__exit = admin_skin_impl.actions.ExitAction.ExitAction(main_frame)
        self.__about = admin_skin_impl.actions.AboutAction.AboutAction(main_frame)

    ##########
    #   Actions
    @property
    def exit(self) -> admin_skin_impl.actions.ExitAction.ExitAction:
        return self.__exit

    @property
    def about(self) -> admin_skin_impl.actions.ExitAction.ExitAction:
        return self.__about
    