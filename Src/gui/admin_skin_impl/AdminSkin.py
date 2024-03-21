import gui.skin as skinapi
import gui.admin_skin_impl.MainFrame as mainfrm
import tkinter as tk

class AdminSkin(skinapi.ISkin):
    """ A database type that uses SQLite as data storage. """
    
    ##########
    #   Constants
    MNEMONIC = 'admin'
    """ The mnemonic identifier of the Admin skin. """

    ##########
    #   Singleton
    __instance :  skinapi.ISkin = None

    def __init__(self):
        assert AdminSkin.__instance is None, 'Use AdminSkin.instance() instead'
        self.__main_frame = mainfrm.MainFrame()
    
    @staticmethod
    def instance() -> 'AdminSkin':
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if AdminSkin.__instance is None:
            AdminSkin.__instance = AdminSkin()
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
        return ((self.__main_frame is not None) and 
                (not self.__main_frame.is_destroyed))

    ##########
    #   ISkin - Operations
    def activate(self) -> None:
        self.__main_frame.activate()

    def deactivate(self) -> None:
        self.__main_frame.deactivate()
            
