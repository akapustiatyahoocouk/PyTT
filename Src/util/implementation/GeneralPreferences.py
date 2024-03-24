#   Internal dependencies on modules within the same component
from util.implementation.Preferences import Preferences
from util.implementation.Annotations import staticproperty
from util.resources.UtilResources import UtilResources

##########
#   Public entities
class GeneralPreferences(Preferences):
    """ The "General" preferences. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Preferences = None

    def __init__(self):
        assert GeneralPreferences.__instance_acquisition_in_progress, "Use GeneralPreferences.instance instead"
        Preferences.__init__(self, Preferences.root, "General")

    @staticproperty
    def instance() -> Preferences:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if GeneralPreferences.__instance is None:
            GeneralPreferences.__instance_acquisition_in_progress = True
            GeneralPreferences.__instance = GeneralPreferences()
            GeneralPreferences.__instance_acquisition_in_progress = False
        return GeneralPreferences.__instance

    ##########
    #   Construction - from derived classes only.
    def __init__(self) -> None:
        Preferences.__init__(self, Preferences.ROOT, "General")

    ##########
    #   Preferences - Properties
    @property
    def display_name(self) -> str:
        return UtilResources.string("Preferences.General")

GeneralPreferences.instance #   to instantiate it
