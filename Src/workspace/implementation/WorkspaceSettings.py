"""
    Persistent settings of the Workspace.
"""
#   Python standard library
from typing import final
from .WorkspaceType import WorkspaceType
from .WorkspaceAddress import WorkspaceAddress

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class WorkspaceSettingsMeta(type):

    ##########
    #   Construction
    def __init__(self, *args, **kwargs):
        type.__init__(self, *args, **kwargs);

        self.__impl = Settings.get("Workspace")

    ##########
    #   Properties
    @property
    def last_workspace_address(self) -> Optional[WorkspaceAddress]:
        workspace_type = WorkspaceType.find_by_mnemonic(self.__impl.get("last_workspace_type", ""))
        if workspace_type is not None:
            external_form = self.__impl.get("last_workspace_address", "")
            try:
                return workspace_type.parse_workspace_address(external_form)
            except:
                return None
        return None

    @last_workspace_address.setter
    def last_workspace_address(self, new_workspace_address: WorkspaceAddress) -> None:
        assert (new_workspace_address is None) or isinstance(new_workspace_address, WorkspaceAddress)
        if new_workspace_address is None:
            self.__impl.remove("last_workspace_type")
            self.__impl.remove("last_workspace_address")
        else:
            self.__impl.put("last_workspace_type", new_workspace_address.workspace_type.mnemonic)
            self.__impl.put("last_workspace_address", new_workspace_address.external_form)

@final
class WorkspaceSettings(metaclass=WorkspaceSettingsMeta):
    """ Persistent settings. """

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
