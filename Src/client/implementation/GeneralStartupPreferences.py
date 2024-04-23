"""
    PyTT Client General/Startup preferences.
"""
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

##########
#   Public entities
class GeneralStartupPreferences(Preferences):
    """ The "General" preferences. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Preferences = None

    def __init__(self):
        assert GeneralStartupPreferences.__instance_acquisition_in_progress, "Use GeneralStartupPreferences.instance instead"
        Preferences.__init__(self, GeneralPreferences.instance, "Startup")

        self.__restore_workspace_on_startup = BoolPreference("RestoreWorkspaceOnStartup", False)
        
        self.add_preference(self.__restore_workspace_on_startup)
        
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

    ##########
    #   Preferences - Operations
    def create_editor(self, parent: tk.BaseWidget) -> tk.BaseWidget:
        assert isinstance(parent, tk.BaseWidget)
        return _Editor(parent)

    ##########
    #   Properties
    @property
    def restore_workspace_on_startup(self) -> BoolPreference:
        return self.__restore_workspace_on_startup

GeneralStartupPreferences.instance #   to instantiate it

##########
#   Implementation helpers
class _Editor(Panel):
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        Panel.__init__(self, parent, **kwargs)
