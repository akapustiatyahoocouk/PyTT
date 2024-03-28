from typing import final

import admin_skin_impl.MainFrame
import admin_skin_impl.actions.ExitAction

@final
class ActionSet:
    
    def __init__(self,
                 main_frame: admin_skin_impl.MainFrame.MainFrame):
        self.__exit = admin_skin_impl.actions.ExitAction.ExitAction(main_frame)

    @property
    def exit(self) -> admin_skin_impl.actions.ExitAction.ExitAction:
        return self.__exit