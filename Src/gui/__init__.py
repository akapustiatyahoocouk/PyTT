print('Loading package', __file__)

#   Dependencies on other PyTT components
from util.interface.api import *

##########
#   Public entities
class GuiSubsystem(LocalizableSubsystem):
    """ The "Ui/GUI" subsustem. """ #   TODO move declarations of ALL subsystems to __init__.py's

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Subsystem = None

    def __init__(self):
        assert GuiSubsystem.__instance_acquisition_in_progress, "Use GuiSubsystem.instance instead"
        LocalizableSubsystem.__init__(self, UiSubsystem.instance)

    @staticproperty
    def instance() -> Subsystem:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if GuiSubsystem.__instance is None:
            GuiSubsystem.__instance_acquisition_in_progress = True
            GuiSubsystem.__instance = GuiSubsystem()
            GuiSubsystem.__instance_acquisition_in_progress = False
        return GuiSubsystem.__instance

    ##########
    #   Subsystem - Properties
    @property
    def display_name(self) -> str:
        from gui.resources.GuiResources import GuiResources
        return GuiResources.string("GuiSubsystem.DisplayName")

    ##########
    #   LocalizableSubsystem - Properties
    @property
    def supported_locales(self) -> set[Locale]:
        from gui.resources.GuiResources import GuiResources
        return GuiResources.factory.supported_locales

##########
#   Instantiate
GuiSubsystem.instance
