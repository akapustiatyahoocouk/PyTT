#   Internal dependencies on modules within the same component
from util.implementation.Preferences import Preferences
from util.implementation.Annotations import staticproperty

##########
#   Public entities
class RootPreferences(Preferences):
    """ The root of the preferences tree. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Preferences = None

    def __init__(self):
        assert RootPreferences.__instance_acquisition_in_progress, "Use RootPreferences.instance instead"
        Preferences.__init__(self, None, "")

    @staticproperty
    def instance() -> Preferences:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if RootPreferences.__instance is None:
            RootPreferences.__instance_acquisition_in_progress = True
            RootPreferences.__instance = RootPreferences()
            RootPreferences.__instance_acquisition_in_progress = False
        return RootPreferences.__instance

    ##########
    #   Preferences - Properties
    @property
    def display_name(self) -> str:
        return ""

RootPreferences.instance    #   To instantiate it
