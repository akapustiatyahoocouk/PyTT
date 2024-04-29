""" Defines "exit PyTT" action. """
#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from .ActionBase import ActionBase
from ..misc.CurrentWorkspace import CurrentWorkspace
from gui.resources.GuiResources import GuiResources
from gui.implementation.views.ViewType import ViewType

##########
#   Public entities
@final
class OpenViewAction(ActionBase):
    """ The "Open a view" action. """

    ##########
    #   Construction
    def __init__(self, view_type: ViewType):
        assert isinstance(view_type, ViewType)
        ActionBase.__init__(self, "Actions.OpenView")
        
        self.__view_type = view_type
        self.name = GuiResources.string("Actions.OpenView.Name").format(view_type.display_name)
        self.small_image = view_type.small_image
        self.large_image = view_type.large_image

    ##########
    #   awt.Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        try:
            self.dialog_parent.open_view(self.__view_type)  #   may fail in some skins!!!
        except Exception as ex:
            ErrorDialog.show(None, ex)
