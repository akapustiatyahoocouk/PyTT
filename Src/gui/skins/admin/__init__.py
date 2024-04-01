"""
    Package declarations for admin_skin_impl package.
"""
print('Loading package', __file__)

#   Python standard library
from typing import final

#   Dependencies on other PyTT components
from gui.api import *
from pnp.api import *
from util.api import *

@final
class AdminSkinPlugin(Plugin):
    
    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Plugin = None

    def __init__(self):
        assert AdminSkinPlugin.__instance_acquisition_in_progress, "Use AdminSkinPlugin.instance instead"
        Plugin.__init__(self)
    
    @staticproperty
    def instance() -> "AdminSkinPlugin":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if AdminSkinPlugin.__instance is None:
            AdminSkinPlugin.__instance_acquisition_in_progress = True
            AdminSkinPlugin.__instance = AdminSkinPlugin()
            AdminSkinPlugin.__instance_acquisition_in_progress = False
        return AdminSkinPlugin.__instance

    ##########
    #   Plugin
    @property
    def display_name(self) -> str:
        return "Admin skin"

    def initialize(self) -> None:
        from gui.skins.SkinRegistry import SkinRegistry
        from gui.skins.admin.AdminSkin import AdminSkin
        SkinRegistry.register_skin(AdminSkin.instance)

AdminSkinPlugin.instance
