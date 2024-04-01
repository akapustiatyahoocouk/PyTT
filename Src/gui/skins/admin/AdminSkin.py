""" Implements the "Admin: skin. """
#   Python standard library

#   Dependencies on other PyTT components
from gui.api import *
from util.api import *

#   Internal dependencies on modules within the same component
from gui.skins.admin.MainFrame import MainFrame # TODO Actions are for ALL skins!

##########
#   Public entities
class AdminSkin(Skin):
    """ A database type that uses SQLite as data storage. """

    ##########
    #   Constants
    MNEMONIC = "admin"
    """ The mnemonic identifier of the Admin skin. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Skin = None

    def __init__(self):
        assert AdminSkin.__instance_acquisition_in_progress, "Use AdminSkin.instance instead"
        Skin.__init__(self)
        self.__main_frame = MainFrame()
        self.__main_frame.deactivate()

    @staticproperty
    def instance() -> "AdminSkin":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if AdminSkin.__instance is None:
            AdminSkin.__instance_acquisition_in_progress = True
            AdminSkin.__instance = AdminSkin()
            AdminSkin.__instance_acquisition_in_progress = False
        return AdminSkin.__instance

    ##########
    #   ISkin - Properties (general)
    @property
    def mnemonic(self) -> str:
        return AdminSkin.MNEMONIC

    @property
    def display_name(self) -> str:
        return 'Admin'

    @property
    def is_active(self) -> bool:
        return (self.__main_frame is not None) and self.__main_frame.winfo_exists

    ##########
    #   ISkin - Operations
    def activate(self) -> None:
        self.__main_frame.activate()

    def deactivate(self) -> None:
        self.__main_frame.deactivate()
