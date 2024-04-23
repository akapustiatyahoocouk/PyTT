"""
    PyTT Client General/Startup preferences.
"""
#   Python standard library

#   Dependencies on other PyTT components
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

GeneralStartupPreferences.instance #   to instantiate it
