"""
    PyTT Client General/Startup preferences.
"""
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from ..resources.ClientResources import ClientResources

##########
#   Public entities
class GeneralStartupPreferences(Preferences):
    """ The "General/Startup" preferences. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Preferences = None

    def __init__(self):
        assert GeneralStartupPreferences.__instance_acquisition_in_progress, "Use GeneralStartupPreferences.instance instead"
        Preferences.__init__(self, GeneralPreferences.instance, "Startup")

        self.__use_last_login = BoolPreference("UseLastLogin", False)
        self.__restore_workspace = BoolPreference("RestoreWorkspace", False)
        
        self.add_preference(self.__use_last_login)
        self.add_preference(self.__restore_workspace)
        
    @staticproperty
    def instance() -> Preferences:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if GeneralStartupPreferences.__instance is None:
            GeneralStartupPreferences.__instance_acquisition_in_progress = True
            GeneralStartupPreferences.__instance = GeneralStartupPreferences()
            GeneralStartupPreferences.__instance_acquisition_in_progress = False
        return GeneralStartupPreferences.__instance

    ##########
    #   Preferences - Properties
    @property
    def display_name(self) -> str:
        return 'Startup'

    @property
    def sort_order(self) -> Optional[int]:
        return 10

    ##########
    #   Preferences - Operations
    def create_editor(self, parent: tk.BaseWidget) -> tk.BaseWidget:
        assert isinstance(parent, tk.BaseWidget)
        return _Editor(parent)

    ##########
    #   Properties
    @property
    def use_last_login(self) -> BoolPreference:
        return self.__use_last_login

    @property
    def restore_workspace(self) -> BoolPreference:
        return self.__restore_workspace

GeneralStartupPreferences.instance #   to instantiate it

##########
#   Implementation helpers
class _Editor(Panel):
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        Panel.__init__(self, parent, **kwargs)

        #   Create controls        
        self.__use_last_login_check_box = CheckBox(self, text=ClientResources.string("GeneralStartupPreferencesEditor.UseLastLoginCheckBox.Text"))
        self.__reload_workspace_check_box = CheckBox(self, text=ClientResources.string("GeneralStartupPreferencesEditor.ReloadWorkspaceCheckBox.Text"))
        
        #   Set up control structure
        self.__use_last_login_check_box.grid(row=0, column=1, padx=2, pady=2, sticky="WE")
        self.__reload_workspace_check_box.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        #   Adjust controls
        self.__use_last_login_check_box.checked = GeneralStartupPreferences.instance.use_last_login.value
        self.__reload_workspace_check_box.checked = GeneralStartupPreferences.instance.restore_workspace.value

        #   Set up event handlers
        self.__use_last_login_check_box.add_action_listener(self.__use_last_login_check_box_clicked)
        self.__reload_workspace_check_box.add_action_listener(self.__reload_workspace_check_box_clicked)

    ##########
    #   Event handlers
    def __use_last_login_check_box_clicked(self, evt: ActionEvent):
        c = self.__use_last_login_check_box.checked
        GeneralStartupPreferences.instance.use_last_login.value = c

    def __reload_workspace_check_box_clicked(self, evt: ActionEvent):
        c = self.__reload_workspace_check_box.checked
        GeneralStartupPreferences.instance.restore_workspace.value = c
