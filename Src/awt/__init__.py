""" The AWT package initialization behaviour. """

print('Loading package', __file__)

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
@final
class AwtSubsystem(LocalizableSubsystem):
    """ The "Ui/AWT" subsustem. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert AwtSubsystem.__instance_acquisition_in_progress, "Use AwtSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, UiSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if AwtSubsystem.__instance is None:
            AwtSubsystem.__instance_acquisition_in_progress = True
            AwtSubsystem.__instance = AwtSubsystem()
            AwtSubsystem.__instance_acquisition_in_progress = False
        return AwtSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from awt.resources.AwtResources import AwtResources
        return AwtResources.string("AwtSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from awt.resources.AwtResources import AwtResources
        return AwtResources.factory.supported_locales

##########
#   Instantiate
AwtSubsystem.instance
